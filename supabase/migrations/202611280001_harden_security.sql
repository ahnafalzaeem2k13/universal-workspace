-- VYBE security and performance hardening.
-- Apply after supabase/schema.sql in the Supabase SQL editor.

-- Index foreign keys and common feed/order filters.
create index if not exists channels_owner_id_idx on public.channels(owner_id);
create index if not exists videos_channel_id_idx on public.videos(channel_id);
create index if not exists videos_published_at_idx on public.videos(published_at desc);
create index if not exists subscriptions_channel_id_idx on public.subscriptions(channel_id);
create index if not exists video_likes_video_id_idx on public.video_likes(video_id);
create index if not exists comments_video_created_idx on public.comments(video_id, created_at desc);
create index if not exists comments_parent_id_idx on public.comments(parent_id);
create index if not exists comments_user_id_idx on public.comments(user_id);
create index if not exists comment_likes_comment_id_idx on public.comment_likes(comment_id);
create index if not exists notifications_user_created_idx on public.notifications(user_id, created_at desc);
create index if not exists playlists_user_id_idx on public.playlists(user_id);
create index if not exists playlist_videos_video_id_idx on public.playlist_videos(video_id);
create index if not exists watch_history_video_id_idx on public.watch_history(video_id);
create index if not exists reports_reporter_id_idx on public.reports(reporter_id);
create index if not exists reports_video_id_idx on public.reports(video_id);
create index if not exists reports_comment_id_idx on public.reports(comment_id);

-- Validate user-submitted video sources at the database boundary too.
do $$
begin
  if not exists (select 1 from pg_constraint where conname = 'videos_youtube_id_format') then
    alter table public.videos add constraint videos_youtube_id_format
      check (youtube_video_id is null or youtube_video_id ~ '^[A-Za-z0-9_-]{11}$');
  end if;
  if not exists (select 1 from pg_constraint where conname = 'videos_direct_mp4_https') then
    alter table public.videos add constraint videos_direct_mp4_https
      check (direct_mp4_url is null or direct_mp4_url ~* '^https://[^[:space:]]+\.mp4([?#].*)?$');
  end if;
  if not exists (select 1 from pg_constraint where conname = 'reports_reason_length') then
    alter table public.reports add constraint reports_reason_length
      check (char_length(reason) between 3 and 100);
  end if;
  if not exists (select 1 from pg_constraint where conname = 'reports_status_allowed') then
    alter table public.reports add constraint reports_status_allowed
      check (status in ('pending', 'under_review', 'resolved', 'rejected'));
  end if;
end $$;

-- Ensure a reply belongs to the same video as its parent comment.
create or replace function public.vybe_validate_comment_parent()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  parent_video uuid;
begin
  if new.parent_id is not null then
    select c.video_id into parent_video
    from public.comments c
    where c.id = new.parent_id;

    if parent_video is null or parent_video <> new.video_id then
      raise exception 'A reply must target a comment on the same video';
    end if;
  end if;
  return new;
end;
$$;

drop trigger if exists vybe_comment_parent_guard on public.comments;
create trigger vybe_comment_parent_guard
before insert or update of parent_id, video_id on public.comments
for each row execute function public.vybe_validate_comment_parent();

-- Authors may edit their own comment text; only the channel owner may pin/unpin.
create or replace function public.vybe_guard_comment_updates()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if coalesce(auth.role(), '') = 'service_role' then
    return new;
  end if;

  if new.body is distinct from old.body
     and old.user_id is distinct from (select auth.uid()) then
    raise exception 'Only the comment author can edit comment text';
  end if;

  if new.pinned is distinct from old.pinned
     and not exists (
       select 1
       from public.videos v
       join public.channels c on c.id = v.channel_id
       where v.id = old.video_id
         and c.owner_id = (select auth.uid())
     ) then
    raise exception 'Only the channel owner can pin or unpin comments';
  end if;

  return new;
end;
$$;

drop trigger if exists vybe_comment_update_guard on public.comments;
create trigger vybe_comment_update_guard
before update on public.comments
for each row execute function public.vybe_guard_comment_updates();

-- Create a profile row for each new authenticated account.
create or replace function public.vybe_handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, username, display_name)
  values (
    new.id,
    'user_' || substr(replace(new.id::text, '-', ''), 1, 12),
    coalesce(nullif(new.raw_user_meta_data ->> 'display_name', ''), 'VYBE user')
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists vybe_on_auth_user_created on auth.users;
create trigger vybe_on_auth_user_created
after insert on auth.users
for each row execute function public.vybe_handle_new_user();

-- Replace permissive policies with least-privilege policies.
drop policy if exists "comment owner update" on public.comments;
drop policy if exists "comment likes owner" on public.comment_likes;
drop policy if exists "notifications owner" on public.notifications;
drop policy if exists "reports insert" on public.reports;

create policy "comment author edits own text"
on public.comments for update
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "channel owner moderates comments"
on public.comments for update
using (
  exists (
    select 1 from public.videos v
    join public.channels c on c.id = v.channel_id
    where v.id = video_id and c.owner_id = (select auth.uid())
  )
)
with check (
  exists (
    select 1 from public.videos v
    join public.channels c on c.id = v.channel_id
    where v.id = video_id and c.owner_id = (select auth.uid())
  )
);

create policy "comment likes are publicly readable"
on public.comment_likes for select using (true);

create policy "comment likes insert own"
on public.comment_likes for insert
with check ((select auth.uid()) = user_id);

create policy "comment likes delete own"
on public.comment_likes for delete
using ((select auth.uid()) = user_id);

create policy "notifications select own"
on public.notifications for select
using ((select auth.uid()) = user_id);

create policy "notifications update own"
on public.notifications for update
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "notifications delete own"
on public.notifications for delete
using ((select auth.uid()) = user_id);

create policy "reports insert pending own"
on public.reports for insert
with check (
  (select auth.uid()) = reporter_id
  and status = 'pending'
  and char_length(reason) between 3 and 100
);

-- Notifications are created by trusted backend code, not arbitrary clients.
revoke all on public.notifications from anon;
revoke insert, update, delete on public.notifications from authenticated;
grant select, delete on public.notifications to authenticated;
grant update (read_at) on public.notifications to authenticated;

-- Restrict updates to the two fields guarded by the trigger above.
revoke update on public.comments from authenticated;
grant update (body, pinned) on public.comments to authenticated;


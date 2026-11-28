# VYBE QA report

Tested with Playwright 1.65.2 / Chromium 159.0.8154.6.

- HTTP 200 at desktop 1440×900, iPad 768×1024, and mobile 390×844.
- Ten demo cards rendered at each viewport; no horizontal overflow.
- No JavaScript page errors observed.
- Passed category filtering, watch page, local likes, comment submission, Shorts view, playlist creation, search page, mobile navigation, manual MP4 import, direct MP4 player rendering, subscription storage, and notification creation.

Run the repeatable suite with `python qa/smoke_test.py` in an environment with Playwright Chromium installed.

Not yet covered: authenticated multi-user flows, Supabase persistence, real API quota behavior, and moderation.

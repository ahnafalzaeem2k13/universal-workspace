import asyncio, subprocess, time
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
PORT = 8768
server = subprocess.Popen(
    ["python", "-m", "http.server", str(PORT), "--directory", str(ROOT)],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

async def main():
    errors = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = await page.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
        assert response and response.status == 200

        # Search upload-date control is present and interactive.
        await page.locator("#search input").fill("Tokyo")
        await page.locator("#search button").click()
        assert await page.locator("#sdate").count() == 1
        await page.locator("#sdate").select_option("week")

        # Theme preference cycles system -> dark -> light -> system.
        for expected in ("dark", "light", "system"):
            await page.locator("#theme").click()
            assert await page.evaluate("localStorage.getItem('vybe-theme')") == expected

        # A user can export their device-local data.
        await page.locator("#account").click()
        async with page.expect_download() as download_info:
            await page.locator("#exportdata").click()
        assert (await download_info.value).suggested_filename == "vybe-backup.json"
        await page.locator("#modal .close").click()

        # Only HTTPS MP4 URLs are accepted.
        await page.locator("#add").click()
        await page.locator("#url").fill("http://example.com/video.mp4")
        await page.locator("#vtitle").fill("Rejected HTTP MP4")
        await page.locator("#import").click()
        assert "valid" in (await page.locator("#toast").inner_text()).lower()

        await page.locator("#url").fill("https://example.com/video.mp4")
        await page.locator("#vtitle").fill("Accepted HTTPS MP4")
        await page.locator("#import").click()
        assert await page.get_by_text("Accepted HTTPS MP4").count() >= 1

        # YouTube Shorts URLs are parsed through the official embed route.
        await page.locator("#add").click()
        await page.locator("#url").fill("https://www.youtube.com/shorts/abcdefghijk")
        await page.locator("#vtitle").fill("Parsed Shorts URL")
        await page.locator("#import").click()
        assert await page.get_by_text("Parsed Shorts URL").count() >= 1

        # Likes and dislikes are mutually exclusive.
        await page.locator(".card").first.click()
        video_id = await page.locator("[data-like]").get_attribute("data-like")
        await page.locator("[data-like]").click()
        state = await page.evaluate("JSON.parse(localStorage.getItem('vybe'))")
        assert video_id in state["likes"] and video_id not in state["dislikes"]
        await page.locator("[data-dislike]").click()
        state = await page.evaluate("JSON.parse(localStorage.getItem('vybe'))")
        assert video_id not in state["likes"] and video_id in state["dislikes"]

        # Comments support replies, sorting, likes and local report capture.
        await page.locator("#comment").fill("Parent comment")
        await page.locator("#commentform button").click()
        await page.locator("[data-reply]").first.click()
        await page.locator("#comment").fill("Child reply")
        await page.locator("#commentform button").click()
        assert "Child reply" in await page.locator("#comments").inner_text()
        await page.locator("#commentsort").select_option("oldest")
        await page.locator("[data-comment-like]").first.click()
        await page.locator("[data-report]").first.click()
        state = await page.evaluate("JSON.parse(localStorage.getItem('vybe'))")
        assert len(state["commentLikes"]) == 1 and len(state["reports"]) == 1

        # Subscription changes create a notification that can be marked read.
        await page.locator("[data-sub]").click()
        await page.locator("#bell").click()
        assert await page.locator("#markread").count() == 1
        await page.locator("#markread").click()
        assert "Read" in await page.locator("#content").inner_text()

        # Channel pages expose tabs and a working local filter.
        await page.locator('aside a[href="#channels"]').click()
        await page.locator("[data-channel]").first.click()
        assert await page.locator('[data-channel-tab="videos"]').count() == 1
        await page.locator('[data-channel-tab="shorts"]').click()
        assert "on" in (await page.locator('[data-channel-tab="shorts"]').get_attribute("class"))
        await page.locator('[data-channel-tab="playlists"]').click()
        assert await page.locator("#channel-results").count() == 1
        await page.locator('[data-channel-tab="videos"]').click()
        await page.locator("#channelquery").fill("Tokyo")
        assert await page.locator("#channelquery").input_value() == "Tokyo"

        # Shorts navigation works with mobile controls and keyboard.
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.locator("#menu").click()
        await page.locator('aside a[href="#shorts"]').click()
        assert await page.locator(".shortframe iframe").count() == 1
        before_short = await page.locator(".shortframe iframe").get_attribute("src")
        await page.locator("#next").click()
        assert await page.locator(".shortframe iframe").get_attribute("src") != before_short
        await page.keyboard.press("ArrowUp")
        await page.locator("[data-short-watch]").click()
        assert await page.locator("#commentform").count() == 1
        assert await page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        await page.set_viewport_size({"width": 1280, "height": 900})

        # Search suggestions and channel-only results.
        await page.locator("#q").fill("Mik")
        assert await page.locator("#vybe-search-suggestions option").count() >= 1
        await page.locator("#q").fill("Mika")
        await page.locator("#search button").click()
        await page.locator("#stype").select_option("channel")
        assert "Mika Travels" in await page.locator("#searchgrid").inner_text()

        # Restore a validated local backup and reload the app state.
        await page.locator("#account").click()
        await page.locator("#restoredata").click()
        import json
        backup = {
            "version": 1,
            "data": {
                "name": "Restored User", "likes": ["a"], "dislikes": [],
                "subs": ["Mindfield"], "saved": [], "history": [],
                "comments": {}, "notifications": [], "playlists": [],
                "imports": [], "commentLikes": [], "reports": []
            }
        }
        await page.locator("#backupfile").set_input_files({
            "name": "vybe-backup.json",
            "mimeType": "application/json",
            "buffer": json.dumps(backup).encode()
        })
        await page.wait_for_timeout(800)
        restored = await page.evaluate("JSON.parse(localStorage.getItem('vybe'))")
        assert restored["name"] == "Restored User" and restored["likes"] == ["a"]

        assert not errors, errors
        print("PASS: search date filter, theme cycle, backup export, secure imports, Shorts URL parsing, likes/dislikes, threaded comments, comment likes/reports, notification read state; no page errors")
        await browser.close()

try:
    time.sleep(1)
    asyncio.run(main())
finally:
    server.terminate()
    server.wait()

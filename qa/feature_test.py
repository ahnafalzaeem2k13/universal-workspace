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

        assert not errors, errors
        print("PASS: search date filter, theme cycle, JSON backup export, HTTPS MP4 validation, YouTube Shorts URL parsing; no page errors")
        await browser.close()

try:
    time.sleep(1)
    asyncio.run(main())
finally:
    server.terminate()
    server.wait()

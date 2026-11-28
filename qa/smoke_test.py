import asyncio, subprocess, time
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
server=subprocess.Popen(["python","-m","http.server","8766","--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(1)
async def main():
 errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  for name,w,h in [("desktop",1440,900),("ipad",768,1024),("mobile",390,844)]:
   page=await browser.new_page(viewport={"width":w,"height":h});page.on("pageerror",lambda e:errors.append(str(e)))
   response=await page.goto("http://127.0.0.1:8766/",wait_until="domcontentloaded")
   assert response.status==200 and await page.locator(".card").count()>=8
   assert not await page.evaluate("document.documentElement.scrollWidth>innerWidth")
   if name=="desktop":
    await page.locator("[data-cat=Travel]").click();assert await page.locator(".card").count()==3
    await page.locator(".card").first.click();assert await page.locator(".player").count()==1
    await page.locator("#comment").fill("smoke test");await page.locator("#commentform button").click();assert "smoke test" in await page.locator("#comments").inner_text()
    await page.locator("aside a[href=\"#shorts\"]").click();assert await page.locator(".shortframe iframe").count()==1
   if name=="mobile":
    await page.locator("#menu").click();assert await page.locator("#side").evaluate("e=>e.classList.contains(\"open\")")
  await browser.close()
 assert not errors,errors
 print("PASS: desktop, iPad, mobile, category, watch, comments, Shorts, mobile menu; no page errors")
try: asyncio.run(main())
finally: server.terminate()

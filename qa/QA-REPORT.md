# VYBE QA report

Tested with Playwright / Chromium in the Google Colab build session.

## Browser and screenshot review

- Desktop 1440×900, iPad 768×1024, and mobile 390×844 each returned HTTP 200.
- Ten video cards rendered at each viewport; document width matched the viewport exactly (no horizontal overflow).
- Full-page screenshots were captured for all three sizes and inspected with OCR/layout checks. The expected navigation, search, category chips, feed headings, video titles, channel names, and metadata were visible. Mobile correctly changed to a single-column feed; iPad used a compact tablet layout.
- No JavaScript page errors were observed.

## Interaction checks

Passed category filtering, watch page, comment submission, Shorts view, mobile navigation, manual MP4 import, direct MP4 player rendering, subscription storage, and notification creation. The earlier regression suite also passed local likes, playlist creation, and search page.

Run the repeatable suite with `python qa/smoke_test.py` in an environment with Playwright Chromium installed.

## Not yet production-verified

Authenticated multi-user flows, Supabase persistence, real YouTube API quota behavior, moderation, and live hosting remain unverified. Browser-local interactions do not sync across devices until Supabase is configured and integrated. The GitHub Pages workflow is present, but the repository's Pages site could not be enabled by the connected GitHub Actions permission; a repository owner must enable Pages / GitHub Actions in repository settings once.

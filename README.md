# rojy-gift

A small anniversary surprise for Rojy, built as a single web page.

Rojy drags a love meter up to 1000%, opens three gifts, and finds a bouquet, a few songs and a letter.

## Files

- `index.html` – the whole page (HTML, CSS and JS in one file, no build step).
- `Rojy_heart_QR.png` – heart-shaped QR code that opens the page.
- `make_heart_qr.py` – script that makes the QR code for any URL.

## Run the page

Open `index.html` in a browser. The fonts load from Google Fonts, so it needs internet to look right.
It is named `index.html`, so GitHub Pages can serve it directly.

## Make a new QR code

```
pip install segno pillow opencv-python numpy
python3 make_heart_qr.py https://your-link-here Rojy_heart_QR.png
```

The script checks that the finished image scans back to the same link.

## Notes

- The songs open on YouTube in a new tab. Pages like this can't embed YouTube, so there is no in-page playback.
- The chick is an original drawing.

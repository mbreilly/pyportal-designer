# PyPortal Display Designer

A WYSIWYG designer for the [Adafruit PyPortal](https://www.adafruit.com/product/4116)'s 320×240 screen. Lay out a clock, date, zip-code weather, a weekly schedule, a "last updated" stamp and your own text labels, add a rotating photo gallery, then export a zip you copy straight onto the `CIRCUITPY` drive.

The preview draws with the same bitmap fonts and 16-bit colors the PyPortal uses, so what you see is what the device shows.

## Use it

Open `index.html` in any browser. It's a single file with no install and no server. Your design is kept in that browser automatically. **Export → Save project** writes a project file you can open again elsewhere.

| Tab | What it does |
| --- | --- |
| Layout | Drag items on the screen; set font (12 choices), size, bold, color and alignment; background color or image; backlight. |
| Schedule | Weekly entries, one line each: days, time, text, e.g. `MTWT 6:40am In DRL until 1:40pm`. Entries can be **At** a time, **From … to …**, or **All day**. Spans and all-day entries are highlighted while they're happening. Also sets the schedule's text and background colors. |
| Gallery | Turn the slideshow on or off, set how long the schedule screen shows before it, upload photos (resized to 320×240) and set seconds per photo, optional clock over the photos. |
| Clock & weather | Weather refresh rate, 12/24-hour time, weather colors, zip code and units. |
| Export | Optional WiFi and OpenWeatherMap key (written only into the zip), drive-space estimate, **Export .zip**. |

## Put it on the PyPortal

1. Install CircuitPython 9 or newer, including 10.x: <https://circuitpython.org/board/pyportal/>. Check `boot_out.txt` on `CIRCUITPY` for the version; 7.x and 8.x are too old.
2. Unzip the export and copy everything onto `CIRCUITPY`: `code.py`, `config.json`, `settings.toml`, `fonts/`, `images/`.
3. Fill in `settings.toml`: `CIRCUITPY_WIFI_SSID`, `CIRCUITPY_WIFI_PASSWORD`, and `OPENWEATHER_KEY` (free at <https://openweathermap.org/api>, Current Weather Data).
4. Add these libraries to `CIRCUITPY/lib` from the library bundle that matches your CircuitPython version (e.g. "Bundle for Version 10.x"), or run
   `circup install adafruit_esp32spi adafruit_requests adafruit_connection_manager adafruit_display_text adafruit_bitmap_font`

The clock is set from the weather request using the zip code's time zone, so it's correct once WiFi connects. After a design change, copying the new `config.json` is enough unless fonts or photos changed.

## Repository layout

```
index.html          the designer, built from the two files below
src/designer.html   designer source (HTML, CSS, JS)
device/code.py      CircuitPython program included in every export
build.py            rebuilds index.html: python3 build.py
examples/           an export of the example design
```

Edit `src/designer.html` or `device/code.py`, then run `python3 build.py`. The designer's schedule and text-placement logic mirrors `code.py` (`schedule_lines`, `make_label`), so change both together.

## How the WYSIWYG match works

- **Fonts:** fonts are rasterized in the browser at the chosen pixel size and exported as BDF files. The preview draws text from those same bitmaps.
- **Placement:** labels are placed with `adafruit_display_text.bitmap_label`, anchored on the text baseline, so positions match the preview pixel for pixel. Text that starts with a glyph hanging left of its origin (e.g. `j`) can be off by a pixel or two.
- **Colors and photos:** colors and photos are quantized to RGB565 in the preview, as on the display. Photos are exported as 24-bit BMPs (about 225 KB each).

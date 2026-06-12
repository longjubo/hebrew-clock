# hebrew-clock

A Hebrew word-clock server that generates 800×480 black-and-white PNG images for e-paper displays. The server expresses the current Israel time in natural written Hebrew, together with an analog clock face, the day/date, and a live weather icon. A companion Arduino sketch drives the image onto a Waveshare 7.5" V2 e-paper panel via a Seeed XIAO ESP32C3.

---

## How It Works

1. The ESP32 fetches a PNG from the server at a configurable interval.
2. The server renders the current Israel time as written Hebrew words (e.g. *שֶׁבַע וָרֶבַע בָּעֶרֶב* — "quarter past seven in the evening"), draws an analog clock and a weather icon, and returns a 1-bit PNG sized exactly 800×480.
3. The ESP decodes the PNG in RAM and writes it to the e-paper display using a mix of partial and full refreshes.

---

## Display Modes

### Normal clock

The main view shows:
- **Analog clock** at the top centre
- **Hebrew time** in large text (hour + minute phrase + time-of-day period)
- **Day name and date** in the bottom-left cell
- **Time-of-day period** (*בַּבֹּקֶר*, *בָּעֶרֶב*, …) in the centre cell
- **Weather** (icon + temperature + condition) in the bottom-right cell

![Normal clock — Heebo-Bold, Raanana](assets/screenshots/clock-main-heebo-raanana.png)
*Heebo-Bold font — Raanana, 22°C partly cloudy*

![Normal clock — NotoSansHebrew-Bold, Tel Aviv](assets/screenshots/clock-main-noto-telaviv.png)
*NotoSansHebrew-Bold font — Tel Aviv*

![Normal clock — FrankRuhlLibre-Bold, Jerusalem](assets/screenshots/clock-main-frankruh-jerusalem.png)
*FrankRuhlLibre-Bold font — Jerusalem, 19°C sunny*

### Morning quiet window (06:00 – 07:30)

Between 06:00 and 07:30 Israel time the display switches to a minimal "do not disturb" screen so early risers are not bothered by the full refresh flicker.

![Morning quiet — Heebo-Bold, Raanana](assets/screenshots/clock-heebo-raanana.png)
*Heebo-Bold font*

![Morning quiet — NotoSansHebrew-Bold, Tel Aviv](assets/screenshots/clock-noto-telaviv.png)
*NotoSansHebrew-Bold font*

![Morning quiet — FrankRuhlLibre-Bold, Jerusalem](assets/screenshots/clock-frankruh-jerusalem.png)
*FrankRuhlLibre-Bold font*

### Night / sleep mode

When `sleeptime=1` is sent by the ESP (during the configured sleep window), the server returns a dark star-field image with a Hebrew "time to sleep" message.

![Night sleep mode](assets/screenshots/clock-sleep.png)

---

## API

The server exposes a single image endpoint at the root path (also reachable as `/clock` or `/clock.png`).

```
GET /?font=<name>&sleeptime=<0|1>&location=<city>
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `font` | `NotoSansHebrew-Bold` | Hebrew font. See [Available Fonts](#available-fonts). |
| `sleeptime` | `0` | Set to `1` to render the night image. |
| `location` | `Tel Aviv` | City passed to the weather API. |

Response: `image/png`, 800×480, 1-bit, `Cache-Control: no-cache`.

Interactive API docs: `http://<host>:8765/api/docs`

### Example URLs

```
# Heebo-Bold, Raanana, normal mode
https://clk.cloudguard.co.il/?font=Heebo-Bold&sleeptime=0&location=Raanana

# Night/sleep image
https://clk.cloudguard.co.il/?font=Heebo-Bold&sleeptime=1
```

---

## Available Fonts

| Font name | Style |
|-----------|-------|
| `NotoSansHebrew-Bold` | Clean modern sans-serif (default) |
| `Heebo-Bold` | Rounded contemporary sans-serif |
| `FrankRuhlLibre-Bold` | Classic serif |
| `FrankRuhlLibre` | Classic serif, regular weight |
| `DavidLibre-Bold` | Traditional Hebrew typeface |

Font files (`.ttf`) must be placed alongside the application (the directory set by the `FONT_DIR` environment variable, default: the project root).

---

## Running with Docker

```yaml
# docker-compose.yml (already included in the repo)
services:
  hebclk:
    build: .
    ports:
      - "8765:8765"
    environment:
      PORT: 8765
      DISPLAY_LAG: 8   # seconds added to displayed time (compensates for refresh delay)
      LOG_LEVEL: info
    restart: unless-stopped
```

```bash
docker compose up -d
```

The container expects font `.ttf` files and `sleeping.png` to be present at build time (the `Dockerfile` copies `*.ttf sleeping.png*` from the project root into `/app/`).

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8765` | Listening port |
| `DISPLAY_LAG` | `8` | Seconds added to Israel time before rendering (accounts for ePaper refresh time) |
| `LOG_LEVEL` | `info` | Loguru log level |
| `FONT_DIR` | app root | Directory containing `.ttf` files |

---

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8765
```

---

## ESP32 Firmware

See **[epaper.md](epaper.md)** for full instructions on:
- Adding the ESP32 board to Arduino IDE
- Installing required libraries
- First-boot Wi-Fi setup
- Web configuration UI reference

![ePaper Configuration UI](assets/screenshots/esp-config-ui.png)

---

## Project Structure

```
app/
  main.py              # FastAPI app + lifespan
  api/v1/router.py     # GET / endpoint
  core/config.py       # Settings (pydantic-settings)
  services/
    clock.py           # Image generation (PIL, Hebrew word-clock logic)
    weather.py         # wttr.in weather cache
sketch/
  hebclk.ino           # ESP32 Arduino sketch
assets/screenshots/    # README images
Dockerfile
docker-compose.yml
requirements.txt
```

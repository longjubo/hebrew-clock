import datetime
from PIL import Image, ImageDraw, ImageFont

def generate_clock_image():
    # גודל המסך של ה-Seeed ESP32 שלך (לרוב 800x480)
    W, H = 800, 480
    img = Image.new("1", (W, H), color=1) # 1 = רקע לבן
    draw = ImageDraw.Draw(img)
    
    # לקיחת זמן נוכחי
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")               # דוגמה: 14:35
    date_str = now.strftime("%A, %B %d, %Y")       # דוגמה: Tuesday, July 07, 2026
    
    # פונט ברירת מחדל של המערכת (לא דורש קבצים חיצוניים ולא קורס)
    font = ImageFont.load_default()
    
    # ציור קו אסתטי באמצע ומסגרת
    draw.rectangle([15, 15, W-15, H-15], outline=0, width=4)
    draw.line([50, H//2 + 20, W-50, H//2 + 20], fill=0, width=2)
    
    # ציור הטקסט (במצב ברירת מחדל הוא קטן, אבל הוא יעבוד מיד)
    draw.text((W//2, H//3), time_str, font=font, fill=0, anchor="mm")
    draw.text((W//2, H//2 + 60), date_str, font=font, fill=0, anchor="mm")
    
    return img

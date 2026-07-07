import os
from PIL import Image, ImageDraw

def generate_clock_image():
    # גודל המסך של ה-Seeed ESP32
    W, H = 800, 480
    
    # מוצא את נתיב התמונה באותה תיקייה של הקוד
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, 'family_sign.png')
    
    try:
        # טוען את התמונה שהעלית
        img = Image.open(image_path)
        # מתאים אותה אוטומטית לגודל המסך שלך
        img = img.resize((W, H))
        # הופך אותה לפורמט דיו אלקטרוני (שחור-לבן מוחלט)
        img = img.convert("1")
        return img
        
    except Exception:
        # מנגנון הגנה: אם שכחת להעלות את התמונה או שהשם לא נכון,
        # המסך לא יקרוס אלא יציג מסגרת שחורה כדי שתדע שהקוד עובד.
        img = Image.new("1", (W, H), color=1)
        draw = ImageDraw.Draw(img)
        draw.rectangle([20, 20, W-20, H-20], outline=0, width=6)
        return img

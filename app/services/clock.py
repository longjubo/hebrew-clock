import io
import urllib.request
from PIL import Image, ImageDraw

def generate_clock_image():
    W, H = 800, 480
    
    # תמונת הנוף הזמנית מהאינטרנט
    image_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=800&auto=format&fit=crop"
    
    try:
        # משתמשים בכלי המובנה של פייתון (אין צורך בהתקנות - לא יקרוס)
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            img_bytes = response.read()
            
        img = Image.open(io.BytesIO(img_bytes))
        img = img.resize((W, H))
        img = img.convert("1")
        return img
        
    except Exception:
        # הגנה מוחלטת: אם יש בעיית אינטרנט, השרת לא יקרוס! הוא פשוט יציג מסגרת שחורה
        img = Image.new("1", (W, H), color=1)
        draw = ImageDraw.Draw(img)
        draw.rectangle([20, 20, W-20, H-20], outline=0, width=6)
        return img

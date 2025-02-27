from PIL import Image, ImageDraw

# Erstelle ein 256x256 Bild mit transparentem Hintergrund
img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Zeichne einen dunklen Kreis als Hintergrund
draw.ellipse([20, 20, 236, 236], fill='#2C2C2C')

# Zeichne ein "T" in der Mitte
draw.text((90, 60), 'T', fill='white', font=ImageFont.truetype('arial.ttf', 120))

# Speichere als ICO
img.save('app/assets/icon.ico', format='ICO') 
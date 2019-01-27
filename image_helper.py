from PIL import Image

def create_thumbnail(image_file, logo_file, out_file):
    background = Image.open(image_file)
    foreground = Image.open("Thumb_Nail_Front.png")
    background.paste(foreground, (0, 0), foreground)
    background.save(out_file,'JPEG')
import io
from PIL import Image, ImageOps, ImageDraw
import urllib.request
image_path = 'https://firebasestorage.googleapis.com/v0/b/img2code-326013.appspot.com/o/login.png?alt=media&token=7ca561c6-9faf-4604-8b05-3b49673157d5'
with urllib.request.urlopen(image_path) as url:
    with open('/tmp/temp.png', 'wb') as f:
        f.write(url.read())
img = Image.open('/tmp/temp.png')
img.show()
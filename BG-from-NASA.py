import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont
import tempfile
from appscript import app, mactypes
import appscript
import subprocess

def doBGfromNASA():
    url =  "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    jsonData = urllib.request.urlopen(url).read()
    contents = json.loads(jsonData)
    imgUrl = contents['hdurl']
    title = contents['title']
    print('found ' + title + " at " + imgUrl)
    f = tempfile.NamedTemporaryFile(delete=True, suffix='.jpg');
    f.write(urllib.request.urlopen(imgUrl).read())
    f.flush()
    img = Image.open(f)
    
    basewidth = 1920.0
    baseheight = 1080.0
    w = img.size[0]
    h = img.size[1]
    factorw = basewidth / w
    factorh = baseheight / h
    factor = min(factorw, factorh)
    if (factor < 1):
      factor = 1.0 /factor
    img = img.resize((int(w / factor), int(h/factor)), Image.Resampling.LANCZOS)
    f2 = tempfile.NamedTemporaryFile(delete=True, suffix='.jpg');
    f2 = open("/tmp/test.jpg", mode="w")
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", img.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype("Arial Unicode.ttf", 30)
    #fnt = ImageFont.load_default()
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((10,80), title, font=fnt, fill=(255,255,255,255))
    img = Image.alpha_composite(img.convert('RGBA'), txt)
    img = img.convert("RGB")
    img.save(f2)
    f2.flush()
    f.close()
    f2.close()
    se = appscript.app('System Events')
    print(f2.name)
    desktops = se.desktops.display_name.get()
    for d in desktops:
        desk = se.desktops[appscript.its.display_name == d]
        desk.picture.set(appscript.mactypes.File(f2.name))
    subprocess.call(['/usr/bin/killall', 'Dock'])
    print("done")
if __name__ == "__main__":
    doBGfromNASA()

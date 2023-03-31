import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont
import tempfile
from appscript import app, mactypes
import appscript

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
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", img.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype("Keyboard.ttf", 40)
    #fnt = ImageFont.load_default()
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((10,10), title, font=fnt, fill=(255,255,255,255))
    out = Image.alpha_composite(img.convert('RGBA'), txt)
    #out.show()    
    se = appscript.app('System Events')
    desktops = se.desktops.display_name.get()
    for d in desktops:
        desk = se.desktops[appscript.its.display_name == d]
        desk.picture.set(appscript.mactypes.File(f.name))
    f.close()
if __name__ == "__main__":
    doBGfromNASA()

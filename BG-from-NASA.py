import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont
import platform
import tempfile
if platform.system().lower().startswith('dar'):
    import appscript
if platform.system().lower().startswith('lin'):
    from linuxdesktop import linuxdesktop
import subprocess

def do_bg_from_nasa():
    url =  "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    json_data = urllib.request.urlopen(url).read()
    contents = json.loads(json_data)
    img_url = contents['hdurl']
    title = contents['title']
    print('found ' + title + " at " + img_url)
    f = tempfile.NamedTemporaryFile(delete=True, suffix='.jpg')
    f.write(urllib.request.urlopen(img_url).read())
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
    #f2 = tempfile.NamedTemporaryFile(delete=True, suffix='.jpg')
    f2 = open("/tmp/test.jpg", mode="w")
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", img.size, (255,255,255,0))

    # get a font
    fontname = "FreeSerif.ttf"
    if platform.system().lower().startswith('dar'):
        fontname = "Arial Unicode.ttf"
    fnt = ImageFont.truetype(fontname, 30)
    #fnt = ImageFont.load_default()
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((10,80), title, font=fnt, fill=(255,255,255,128))
    img = Image.alpha_composite(img.convert('RGBA'), txt)
    img = img.convert("RGB")
    img.save(f2)
    f2.flush()
    f.close()
    f2.close()
    print(f2.name)
    if platform.system().lower().startswith('dar'):
        se = appscript.app('System Events')
        desktops = se.desktops.display_name.get()
        for d in desktops:
            desk = se.desktops[appscript.its.display_name == d]
            desk.picture.set(appscript.mactypes.File(f2.name))
            subprocess.call(['/usr/bin/killall', 'Dock'])
    if platform.system().lower().startswith('lin'):
        lde = linuxdesktop()
        lde.set_wallpaper(file_loc=f2.name, first_run=1)
    print("done")
if __name__ == "__main__":
    do_bg_from_nasa()

import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont

def doBGfromNASA():

    tmpName="C:\\temp\\tmpPyImg.jpg"

    url =  "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    jsonData = urllib.request.urlopen(url).read()
    contents = json.loads(jsonData)
    imgUrl = contents['hdurl']
    title = contents['title']
    print('found ' + title + " at " + imgUrl)
    f = open(tmpName, 'wb')
    f.write(urllib.request.urlopen(imgUrl).read())
    f.close()
    img = Image.open(tmpName)
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", img.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype("arial.ttf", 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((10,10), title, font=fnt, fill=(255,255,255,255))
    out = Image.alpha_composite(img.convert('RGBA'), txt)

    out.show()    

if __name__ == "__main__":
    doBGfromNASA()

from pymongo import MongoClient, GEO2D
from PIL import Image

db = MongoClient('45.79.159.210', 27017).fandemic
products = db.sample_products.find({'category': 'fitness'})
logo = Image.open("rx.png")
dis = Image.open("dis.png")


for product in products:

    url = 'fandemic/website/static/img/sample_products/fitness/'+product['default_img'][0]
    background = Image.open(url).convert("RGBA")
    bw, bh = background.size

    maxsize = (bw*.50, bh*.10)
    logo.thumbnail(maxsize, Image.ANTIALIAS)
    lw, lh = logo.size

    img = logo.convert("RGBA").rotate( -16, expand=1,resample=Image.BICUBIC )
    logomask = logo.convert("RGBA").rotate( -16, expand=1 ,resample=Image.BICUBIC)
    data = img.getdata()

    newData = []
    for item in data:
        if item[3] > 200:
            newData.append((item[0], item[2], item[1], 200))
        else:
            newData.append(item)

    img.putdata(newData)

    background.paste(logomask, (int(bw*.66-(lw/2)), int(bh*.515-(lh/2))), img)
    background.save('test/'+product['sku']+'.png', 'PNG', dpi=[72,72])

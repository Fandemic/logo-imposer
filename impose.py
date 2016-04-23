from pymongo import MongoClient, GEO2D
from PIL import Image

db = MongoClient('45.79.159.210', 27017).fandemic
products = db.sample_products.find({'category': 'fitness'})


for product in products:

    logo = Image.open("smallerlogo.png")

    url = '../website/static/img/sample_products/fitness/'+product['default_img'][0]
    background = Image.open(url).convert("RGBA")
    bw, bh = background.size

    i = product['impose']

    maxsize = (int(bw*i['w']), int(bh*i['h']))
    logo.thumbnail(maxsize, Image.ANTIALIAS)
    lw, lh = logo.size

    img = logo.convert("RGBA").rotate( i['a'], expand=1,resample=Image.BICUBIC )
    logomask = logo.convert("RGBA").rotate( i['a'], expand=1 ,resample=Image.BICUBIC)
    data = img.getdata()

    newData = []
    for item in data:
        if item[3] > 200:
            newData.append((item[0], item[2], item[1], 110))
        else:
            newData.append(item)

    img.putdata(newData)

    background.paste(logomask, (int(bw*i['x']-(lw/2)), int(bh*i['y']-(lh/2))), img)
    background.save('test/'+product['sku']+'.png', 'PNG', dpi=[72,72])

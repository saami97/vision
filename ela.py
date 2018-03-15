from PIL import Image, ImageChops, ImageEnhance
import sys, os.path

def elaanalysis(filepath):
    absfilename = filepath.filename.split('/')
    filename = os.path.join('static/photoshopped/',absfilename[1])
    filepath.save(filename)
    resaved = filename + '.resaved.jpg'
    ela = filename + '.ela.png'

    im = Image.open(filename)

    im.save(resaved, 'JPEG', quality=90)
    resaved_im = Image.open(resaved)

    ela_im = ImageChops.difference(im, resaved_im)
    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0/max_diff

    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
    if(max_diff > 30):
        ela_im.save(ela)

    return max_diff

import qrtools
from pdf2image import convert_from_path
import sys

qr = qrtools.QR()

filename = "dirty"
if len(sys.argv) > 1: filename = sys.argv[1]
fullpath = f"/home/andreu/botellot/examples/files/{filename}.pdf"

images = convert_from_path(fullpath)

# Save pages as images in the pdf
for i in range(len(images)):
    pagename = filename + str(i)
    pagepath = f"/home/andreu/botellot/examples/files/{pagename}.jpg"
    
    images[i].save(pagepath, 'JPEG')
    qr.decode(filename=pagepath)
    print(qr.data)
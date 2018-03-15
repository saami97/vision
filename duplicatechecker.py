import hashlib
import cv2
import os
from PIL import Image
import mmap
import MySQLdb as db

dbConfig = {
    'user' : 'root',
    'passwd' : 'bombaydeing27',
    'host' : '127.0.0.1',
    'db' : 'eyecare'
}



def insertPre(imgPath,prepost,dbConfig=dbConfig):
    conn = db.connect(**dbConfig)
    cur = conn.cursor()
    query = "INSERT INTO {pp} VALUES(null,'{hashString}');"
    img = Image.open(imgPath)
    hashedString = dhash(img)
    if(isDuplicate(prepost,hashedString,dbConfig)):
        return False
    else:
        query = query.format(pp=prepost,hashString=hashedString)
        cur.execute(query)
        cur.close()
        conn.commit()
        conn.close()
        return True


#hashing algo
def dhash(image, hash_size = 8):
        # Grayscale and shrink the image in one step.
        image = image.convert('L').resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS,
        )
        pixels = list(image.getdata())
# Compare adjacent pixels.
        difference = []
        for row in xrange(hash_size):
            for col in xrange(hash_size):
                pixel_left = image.getpixel((col, row))
                pixel_right = image.getpixel((col + 1, row))
                difference.append(pixel_left > pixel_right)
        # Convert the binary array to a hexadecimal string.
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
        return ''.join(hex_string)

def isDuplicate(prepost,imageHash,dbConfig):
    conn = db.connect(**dbConfig)
    cur = conn.cursor()
    query = "select * from {prep} where imageHash='{hash}'"
    query = query.format(prep=prepost,hash=imageHash)
    print(query)
    cur.execute(query)
    row = cur.fetchall()
    if(not row):
        return False
    else:
        return True
    cur.close()

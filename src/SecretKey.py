# -*- coding:utf-8 -*-

from Crypto import Random
from PIL import Image

from Util import *

# 3 pixel save 1 byte
def generateKey(img):
    imgMode = img.mode

    if len(imgMode) != 3:
        print 'the Mode of image is not RGB'
        return None

    (w, h) = img.size

    if w * h < 102:
        print 'the Image is too small, image size w * h must >= 102'
        return None

    # random generate key and iv
    rndfile = Random.new()
    keyData = rndfile.read(16)
    ivData = rndfile.read(16)

    # byte to binary string
    dataList = []
    for i in keyData:
        byteList = byte2Bin(ord(i))
        dataList.append(byteList)
    for i in ivData:
        byteList = byte2Bin(ord(i))
        dataList.append(byteList)

    pixArray = img.load()
    # first 3 pixel, write the KEY_MODE value
    modeByteList = byte2Bin(KEY_MODE)
    channelList = []
    for i in range(3):
        x = i / w
        y = i % w
        (R, G, B) = pixArray[x, y]
        channelList.append(R)
        channelList.append(G)
        channelList.append(B)
    for i in range(8):
        pv = channelList[i]
        pv = pv & 0xfe | modeByteList[i]
        channelList[i] = pv
    for i in range(3):
        x = i / w
        y = i % w
        (R, G, B) = (channelList[i * 3], channelList[i * 3 + 1], channelList[i * 3 + 2])
        pixArray[x, y] = (R, G, B)

    for dataIndex in range(32):
        dataByteList = dataList[dataIndex]
        channelList = []
        for i in range(3):
            pixIndex = 3 + dataIndex * 3 + i
            x = pixIndex / w
            y = pixIndex % w
            (R, G, B) = pixArray[x, y]
            channelList.append(R)
            channelList.append(G)
            channelList.append(B)

        for i in range(8):
            pv = channelList[i]            
            pv = pv & 0xfe | dataByteList[i]
            channelList[i] = pv

        for i in range(3):
            pixIndex = 3 + dataIndex * 3 + i
            x = pixIndex / w
            y = pixIndex % w
            (R, G, B) = (channelList[i * 3], channelList[i * 3 + 1], channelList[i * 3 + 2])
            pixArray[x, y] = (R, G, B)


    return img

def extractKey(img):
    imgMode = img.mode

    if len(imgMode) != 3:
        print 'the Mode of image is not RGB'
        return None

    (w, h) = img.size

    if w * h < 102:
        print 'the Image is too small, image size w * h must >= 102'
        return None

    pixArray = img.load()
    # check the mode is KEY_MODE
    channelList = []
    modeValue = 0
    for i in range(3):
        x = i / w
        y = i % w
        (R, G, B) = pixArray[x, y]
        channelList.append(R)
        channelList.append(G)
        channelList.append(B)
    for i in range(8):
        bit = channelList[i] & 0x01
        modeValue = modeValue * 2 + bit

    if modeValue != KEY_MODE:
        print 'the image is not save secrect key'
        return None

    # calc the key data
    keyData = []
    for keyIndex in range(16):
        keyValue = 0
        channelList = []
        for i in range(3):
            pixIndex = 3 + keyIndex * 3 + i
            x = pixIndex / w
            y = pixIndex % w
            (R, G, B) = pixArray[x, y]
            channelList.append(R)
            channelList.append(G)
            channelList.append(B)
        for i in range(8):
            bit = channelList[i] & 0x01
            keyValue = keyValue * 2 + bit
        keyData.append(chr(keyValue))

    ivData = []
    for ivIndex in range(16):
        ivValue = 0
        channelList = []
        for i in range(3):
            pixIndex = 51 + ivIndex * 3 + i
            x = pixIndex / w
            y = pixIndex % w
            (R, G, B) = pixArray[x, y]
            channelList.append(R)
            channelList.append(G)
            channelList.append(B)
        for i in range(8):
            bit = channelList[i] & 0x01
            ivValue = ivValue * 2 + bit
        ivData.append(chr(ivValue))

    return (''.join(keyData), ''.join(ivData))

if __name__ == '__main__':
    import sys
    img = Image.open(sys.argv[1])
    newImg = generateKey(img)
    print extractKey(newImg)

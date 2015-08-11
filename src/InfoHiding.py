# -*- coding:utf-8 -*-

import os

from Util import *

# 3 pixel save 1 byte
def encode_data(img, data):
    imgMode = img.mode
    if len(imgMode) != 3:
        print 'the Mode of image is not RGB'
        return None
    (w, h) = img.size
    countData = len(data)
    print countData
    storeSize = 4 + countData * 3
    if w * h < storeSize:
        print 'the Image is too small, cannot hide all the data!'
        return None


    # byte to binary string
    dataList = []
    for i in data:
        byteList = byte2Bin(ord(i))
        dataList.append(byteList)

    pixArray = img.load()
    # first 3 pixel, write the INFO_MODE value
    modeByteList = byte2Bin(INFO_MODE)
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

    # write the number of data
    countDataList = num2Bin_32(countData)
    channelList = []
    for i in range(6):
        x = (i + 3) / w
        y = (i + 3) % w
        (R, G, B) = pixArray[x, y]
        channelList.append(R)
        channelList.append(G)
        channelList.append(B)
    for i in range(8):
        pv = channelList[i]
        pv = pv & 0xfe | countDataList[i]
        channelList[i] = pv

        pv_1 = channelList[i + 9]
        pv_1 = pv_1 & 0xfe | countDataList[i + 8]
        channelList[i + 9] = pv_1        

    for i in range(6):
        x = (i + 3) / w
        y = (i + 3) % w
        (R, G, B) = (channelList[i * 3], channelList[i * 3 + 1], channelList[i * 3 + 2])
        pixArray[x, y] = (R, G, B)

    # hide the info
    for dataIndex in range(countData):
        dataByteList = dataList[dataIndex]
        channelList = []
        for i in range(3):
            pixIndex = 9 + dataIndex * 3 + i
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
            pixIndex = 9 + dataIndex * 3 + i
            x = pixIndex / w
            y = pixIndex % w
            (R, G, B) = (channelList[i * 3], channelList[i * 3 + 1], channelList[i * 3 + 2])
            pixArray[x, y] = (R, G, B)

    return img

# 
def decode_data(img):
    imgMode = img.mode

    if len(imgMode) != 3:
        print 'the Mode of image is not RGB'
        return None

    (w, h) = img.size

    pixArray = img.load()
    # check the mode is INFO_MODE
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

    if modeValue != INFO_MODE:
        print 'the image is not save secrect key'
        return None

    # calc the data number
    numValue = 0
    channelList = []
    for i in range(3, 9, 1):
        x = i / w
        y = i % w
        (R, G, B) = pixArray[x, y]
        channelList.append(R)
        channelList.append(G)
        channelList.append(B)
    for i in range(8):
        bit = channelList[i] & 0x01
        numValue = numValue * 2 + bit
    for i in range(9, 17, 1):
        bit = channelList[i] & 0x01
        numValue = numValue * 2 + bit
    print numValue

    # infoDatas = bytearray(numValue)
    infoDatas = []
    for dataIndex in range(numValue):
        byteValue = 0
        channelList = []
        for i in range(3):
            pixIndex = 9 + dataIndex * 3 + i
            x = pixIndex / w
            y = pixIndex % w
            (R, G, B) = pixArray[x, y]
            channelList.append(R)
            channelList.append(G)
            channelList.append(B)
        for i in range(8):
            bit = channelList[i] & 0x01
            byteValue = byteValue * 2 + bit
        #infoDatas[dataIndex] = byteValue
        infoDatas.append(chr(byteValue))

    return ''.join(infoDatas)

# encrypt text
def encrypt_text(text, encryptor):
    datas = bytearray(text, 'utf-8')
    dataLen = len(datas)
    if dataLen == 0:
        print 'text is empty'
        return None
    temp = dataLen % 16
    if temp > 0:
        spaceNum = 16 - temp
        for i in range(spaceNum):
            datas.append(32)
    encryptDatas = encryptor.encrypt(datas.decode(encoding = 'utf-8'))

    return encryptDatas

# decrypt text
def decrypt_data(data, decryptor):
    plainDatas = decryptor.decrypt(data)

    return plainDatas

def encrypt_file(file, encryptor):
    datas = file.read()
    dataLen = len(datas)
    if dataLen == 0:
        print 'file is empty'
        return None
    temp = dataLen % 16
    if temp > 0:
        spaceNum = 16 - temp
        tempStr = ''
        for i in range(spaceNum):
            tempStr = '%s ' % tempStr
        datas = '%s%s' % (datas, tempStr)

    encryptDatas = encryptor.encrypt(datas)

    return encryptDatas

if __name__ == "__main__":
    from PIL import Image
    from Crypto.Cipher import AES
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')


    img = Image.open(sys.argv[1])
    #text = sys.argv[2]
    #
    pFile = open(sys.argv[2])

    # print len(text)
    key = '1234567891234560'
    obj = AES.new(key, AES.MODE_CBC, key)
    obj2 = AES.new(key, AES.MODE_CBC, key)
    ed = encrypt_file(pFile, obj)
    encode_data(img, ed)
    imgd = decode_data(img)
    pd = decrypt_data(imgd, obj2)
    saveFile = open(sys.argv[3], 'w')
    saveFile.writelines(pd)
    saveFile.close()
    # print len(ed)
    # print ord(ed[0])
    # pd = decrypt_text(ed, obj2)
    # print len(pd)
    # print '%s|' % pd
    # datas = bytearray(text, 'utf-8')
    # print len(datas)

    # encode_data(img, datas)
    # extractDatas = decode_data(img)
    # print extractDatas.decode(encoding = "utf-8")

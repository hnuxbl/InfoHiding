# -*- coding:utf-8 -*-

# byte to binary string

KEY_MODE = 47
INFO_MODE = 137

def byte2Bin(byte):
    if byte > 255 or byte < 0:
        print "single byte's value between 0 and 255"
        return None
    else:
        bitList = []
        for i in range(8):
            bit = byte & 0x01
            bitList.insert(0, bit)
            byte >>= 1

        return bitList

def num2Bin_32(num):
    if num > 65535 or num < 0:
        print "The num's value between 0 and 65535"
        return None
    else:
        bitList = []
        for i in range(16):
            bit = num & 0x01
            bitList.insert(0, bit)
            num >>= 1

        return bitList

if __name__ == "__main__":
    print num2Bin_32(35)

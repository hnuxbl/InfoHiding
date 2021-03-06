# -*- coding=utf-8 -*-

from Tkinter import *
import tkFileDialog, tkMessageBox
from PIL import Image, ImageTk
from InfoHiding import *
from SecretKey import extractKey

from Crypto.Cipher import AES
from os.path import getsize

class FileHideFrame:

    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row = 0, column = 0)

        self.dataPhoto = None
        self.dataImage = None
        self.keyPhoto = None
        self.keyImage = None
        self.encryptDone = False
        self.decryptDone = False
        self.decryptData = None
        self.filePath = None

        self.chooseDataBtn = Button(self.frame, text = "Data Image", command = self.chooseDataImage)
        self.chooseDataBtn.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10)

        self.chooseKeyBtn = Button(self.frame, text = "Key Image", command = self.chooseKeyImage)
        self.chooseKeyBtn.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10)

        self.dataCanvas = Canvas(self.frame, width = 400, height = 300, bg = 'white')
        self.dataCanvas.grid(row = 0, column = 2, columnspan = 3, rowspan = 4, sticky = SE, padx = 10, pady = 10)

        self.keyCanvas = Canvas(self.frame, width = 400, height = 300, bg = 'white')
        self.keyCanvas.grid(row = 0, column = 5, columnspan = 3, rowspan = 4, sticky = SE, padx = 10, pady = 10)

        self.operation = IntVar()
        self.operation.set(1)
        self.encrytBtn = Radiobutton(self.frame, text = "Encryt", variable = self.operation, value = 1)
        self.encrytBtn.grid(row = 5, column = 0)
        self.decrytBtn = Radiobutton(self.frame, text = "Decryt", variable = self.operation, value = 2)
        self.decrytBtn.grid(row = 5, column = 1)

        self.runBtn = Button(self.frame, text = "Run", command = self.run)
        self.runBtn.grid(row = 6, column = 0)
        self.saveBtn = Button(self.frame, text = "Save", command = self.saveImg)
        self.saveBtn.grid(row = 6, column = 1)

        # self.textBox = Text(self.frame, width = 117, height = 10)
        # self.textBox.grid(row = 4, column = 2, columnspan = 6, rowspan = 4, sticky = SE, padx = 10, pady = 10)
        self.chooseFileBtn = Button(self.frame, text = "Choose File ......", command = self.chooseDataFile)
        self.chooseFileBtn.grid(row = 4, column = 2, columnspan = 6, rowspan = 2,sticky = W, padx = 10, pady = 10)
        self.pathLabel = Label(self.frame, text = "")
        self.pathLabel.grid(row = 6, column = 2, columnspan = 6, rowspan = 2,sticky = W, padx = 10, pady = 10)


    def chooseDataImage(self):
        imgPath = tkFileDialog.askopenfilename(parent = self.frame, initialdir = '/home/st/Pictures', title = 'Choose One Data Image', filetypes = [('BMP', '.bmp'), ('PNG', '.png')])
        if imgPath != "":
            self.dataImage = Image.open(imgPath)
            imgMode = self.dataImage.mode
            (w, h) = self.dataImage.size
            if len(imgMode) != 3:
                tkMessageBox.showwarning('Warnings', 'Please choose one 3 channel color image\nYour choise mode is ' + str(imgMode))
                self.dataImage = None
            elif w * h < 15:
                tkMessageBox.showwarning('Warnings', "The image's size w * h must > 15")
                self.dataImage = None
            else:
                thumbImg = self.dataImage.copy()
                thumbImg.thumbnail((400, 300))
                self.dataPhoto = ImageTk.PhotoImage(thumbImg)
                self.dataCanvas.create_image(200, 150, image = self.dataPhoto)

    def chooseKeyImage(self):
        imgPath = tkFileDialog.askopenfilename(parent = self.frame, initialdir = '/home/st/Pictures', title = 'Choose One Key Image', filetypes = [('BMP', '.bmp'), ('PNG', '.png')])
        if imgPath != "":
            self.keyImage = Image.open(imgPath)
            imgMode = self.keyImage.mode
            (w, h) = self.keyImage.size
            if len(imgMode) != 3:
                tkMessageBox.showwarning('Warnings', 'Please choose one 3 channel color image\nYour choise mode is ' + str(imgMode))
                self.keyImage = None
            elif w * h < 102:
                tkMessageBox.showwarning('Warnings', "The image's size w * h must > 102")
                self.keyImage = None
            else:
                thumbImg = self.keyImage.copy()
                thumbImg.thumbnail((400, 300))
                self.keyPhoto = ImageTk.PhotoImage(thumbImg)
                self.keyCanvas.create_image(200, 150, image = self.keyPhoto)


    def chooseDataFile(self):
        path = tkFileDialog.askopenfilename(parent = self.frame, initialdir = '/home/st/', title = 'Choose One Data File')
        if path != "":
            fileSize = getsize(path)
            
            if fileSize > 65535:
                tkMessageBox.showwarning('Warnings', 'The size of data file must <= 63k')
            else:
                self.filePath = path
                self.pathLabel['text'] = path

    def run(self):
        
        if self.dataImage is None:
            tkMessageBox.showwarning('Warnings', 'Please choose one Data image firstly!')
        elif self.keyImage is None:
            tkMessageBox.showwarning('Warnings', 'Please choose one Key image!')
        else:
            extractData = extractKey(self.keyImage)
            if extractData is None:
                tkMessageBox.showwarning('Warnings', 'The key image your choose is not correct!')
            else:
                key = extractData[0]
                iv = extractData[1]
                aesObj = AES.new(key, AES.MODE_CBC, iv)
                op = self.operation.get()
                if op == 1:
                    if self.filePath is None:
                        tkMessageBox.showwarning('Warnings', 'Please choose One Data File!')
                    else:
                        dataFile = open(self.filePath)
                        encryptData = encrypt_file(dataFile, aesObj)
                        encode_data(self.dataImage, encryptData)
                        self.encryptDone = True
                        tkMessageBox.showinfo('Infos', 'File Hiding Success!')
                else:
                    encodeData = decode_data(self.dataImage)
                    if encodeData is None:
                        tkMessageBox.showwarning('Warnings', 'The Data image your choose is not correct!')
                    else:
                        self.decryptData = decrypt_data(encodeData, aesObj)
                        self.decryptDone = True
                        tkMessageBox.showinfo('Infos', 'File Decrypt Success!')
        # else:
        #     tkMessageBox.showwarning('Warnings', 'Please choose one image')



    def saveImg(self):
        if self.operation.get() == 1 and self.encryptDone:
            savePath = tkFileDialog.asksaveasfilename(parent = self.frame, initialdir = '/home/st/Pictures', title = 'Save Encryted Data Image', filetypes = [('BMP', '.bmp'), ('PNG', '.png')])
            if savePath != "":
                self.dataImage.save(savePath)
                tkMessageBox.showinfo('Infos', 'Encrypted Image Save Success!\npath: %s' % savePath)
        elif self.operation.get() == 2 and self.decryptData is not None:
            savePath = tkFileDialog.asksaveasfilename(parent = self.frame, initialdir = '/home/st/', title = 'Save Decryted Data File')
            if savePath != "":
                saveFile = open(savePath, 'w')
                saveFile.writelines(self.decryptData)
                saveFile.close()
                tkMessageBox.showinfo('Infos', 'Dncrypted Data File Save Success!\npath: %s' % savePath)


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')

    root = Tk()
    root.title('File Hiding Tool')
    FileHideFrame = FileHideFrame(root)

    root.mainloop()

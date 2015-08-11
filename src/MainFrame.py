from Tkinter import *

from TextHideFrame import TextHideFrame
from FileHideFrame import FileHideFrame
from KeyGenFrame import KeyGenerateFrame

root = Tk()

def textFrame():
	textHideFrame = TextHideFrame(root)

def fileFrame():
	fileHideFrame = FileHideFrame(root)

def KeyFrame():
	keyGenFrame = KeyGenerateFrame(root)

# create a toplevel menu
menubar = Menu(root)
menubar.add_command(label = "TextHide", command = textFrame)
menubar.add_command(label = "FileHide", command = fileFrame)
menubar.add_command(label = "KeyGen", command = KeyFrame)
menubar.add_command(label = "Quit", command = root.quit)

# display the menu
root.config(menu = menubar, width = 400, height = 400)

root.mainloop()

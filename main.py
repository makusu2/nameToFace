import tkinter
from tkinter import *
import generateXML
import createHTML
import os
class Main:
    def __init__(self):
        self.wind=Tk()
        #root.withdraw()
       # self.wind=Toplevel(root)
        #self.wind.protocol("WM_DELETE_WINDOW",root.destroy)
        self.wind.xmlButton = Button(self.wind,text="Generate XML",command=self.generateXML)
        self.wind.htmlButton = Button(self.wind,text="Create HTML page",command=self.createHTML)
        self.wind.openButton = Button(self.wind,text="View HTML page",command=self.openHTML)
        self.wind.xmlButton.pack()
        self.wind.htmlButton.pack()
        self.wind.openButton.pack()
        #self.pack()
        self.wind.title("makuDirectory")
        self.wind.geometry('{}x{}'.format(200,200))
        #self.withdraw()
        #input("Press Enter to continue...")
        mainloop()
    def generateXML(self):
        generateXML.main(mainWindow=self.wind)
    def createHTML(self):
        createHTML.main(mainWindow=self.wind)
    def openHTML(self):
        os.system("start htmlPeople.html")
main = Main()
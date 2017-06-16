import tkinter
from tkinter import *
import generateXML
import createHTML
import os
class Main(Tk):
    def __init__(self,*args,**kargs):
        Tk.__init__(self,*args,**kargs)
        self.xmlButton = Button(self,text="Generate XML",command=self.generateXML)
        self.htmlButton = Button(self,text="Create HTML page",command=self.createHTML)
        self.xmlButton.pack()
        self.htmlButton.pack()
        self.title("makuDirectory")
        self.geometry('{}x{}'.format(200,200))
        mainloop()
    def generateXML(self):
        generateXML.main(mainWindow=self)
    def createHTML(self):
        createHTML.main(mainWindow=self)
    def openHTML(self):
        os.system("start htmlPeople.html")
main = Main()
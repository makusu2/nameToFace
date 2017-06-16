import tkinter
from tkinter import *
import generateXML
import createHTML
import os
class Main(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.xmlButton = Button(self,text="Generate XML",command=self.generateXML)
        self.htmlButton = Button(self,text="Create HTML page",command=self.createHTML)
        self.openButton = Button(self,text="View HTML page",command=self.openHTML)
        self.xmlButton.pack()
        self.htmlButton.pack()
        self.openButton.pack()
        self.title("makuDirectory")
        self.geometry('{}x{}'.format(200,200))
        mainloop()
    def generateXML(self):
        generateXML.main()
    def createHTML(self):
        createHTML.main()
    def openHTML(self):
        os.system("start htmlPeople.html")
main = Main()
import tkinter as tk
from tkinter import filedialog
import os
import sys
from os.path import isfile, join
import PIL
from PIL import Image, ImageTk
from resizeimage import resizeimage
import xml.etree.ElementTree as ET
import xml.dom.minidom
class Main(tk.Tk):
    def __init__(self,*args,**kargs):
        tk.Tk.__init__(self,*args,**kargs)
        self.xmlButton = tk.Button(self,text="Generate XML",command=self.generateXML)
        self.htmlButton = tk.Button(self,text="Create HTML page",command=self.createHTML)
        self.xmlButton.pack()
        self.htmlButton.pack()
        self.title("makuDirectory")
        self.geometry('{}x{}'.format(200,200))
        tk.mainloop()
    def generateXML(self):
        createXML(mainWindow=self)
    def createHTML(self):
        createHTML(mainWindow=self)
def createHTML(mainWindow=None):
    tree=ET.parse(filedialog.askopenfilename(parent=mainWindow,title="Please open the XML file of the employees."))
    root=tree.getroot()
    people = [{'firstName':person.find('FirstName').text,'lastName':person.find('LastName').text,'job':person.find('Job').text,'path':person.find('Path').text} for person in root]
    s="<!DOCTYPE html>\n<html>\n<body>\n"
    for i,person in enumerate(people):
        colNum=i%3
        assert colNum in [0,1,2]
        personName = person['firstName']+" "+person['lastName']
        innerString="\t\t\t\t<img src=\""+person['path']+"\" style=\"width: 250px; height: 250px;\" />\n\t\t\t\t<center>"+personName+"</center>\n\t\t\t\t<center>"+person['job']+"</center>\n\t\t\t\t<p />\n"
        if colNum==0:s+="\t<div class=\"row\">\n\t\t<div class=\"col-md-12\">\n\t\t\t<div style=\"float: left; width: 33%;\">\n"
        elif colNum==1:s+="\t\t\t<div style=\"float: right; width: 33%;\">\n"
        else:s+="\t\t\t<div style=\"display: inline-block; width: 33%;\">\n"
        s+=innerString+"\t\t\t</div>\n"
        if colNum==2 or i==len(people)-1:
            s+="\t\t</div>\n\t</div>\n</body>\n</html>\n"
    file=filedialog.asksaveasfile(master=mainWindow,title="Please enter the name of which the HTML file should be saved")
    file.write(s)
    file.close()
    
    
    
    
class MainRoot(tk.Toplevel):
    def __init__(self,*args,**kwargs):
        tk.Toplevel.__init__(self,*args,**kwargs)
        self.master=kwargs.get('master')
        self.paths = self.getPaths()
        self.people = [Person(path) for path in self.paths]
        self.forms = [Form(self,person=person) for person in self.people]
        self.currentForm = 0
        self.lift()
        self.forms[self.currentForm].focusOn()
    def getPaths(self):
        picturesDirectory = filedialog.askdirectory(parent=self,initialdir="/", title="Please select the directory of the images",master=self.master)
        dirContents = [picturesDirectory+"/"+file for file in os.listdir(picturesDirectory)]
        filePaths = [path for path in dirContents if isfile(path)]
        return filePaths
    def submitted(self):
        self.forms[self.currentForm].focusOff()
        if self.currentForm==len(self.forms)-1:
            self.completedForms()
        else:
            self.currentForm+=1
            self.forms[self.currentForm].focusOn()
    def completedForms(self):
        file = filedialog.asksaveasfile(mode='w',defaultextension=".xml",master=self.master,title="Where would you like to save the XML file?")
        file.write(generateXML(self.people))
        file.close()
        self.destroy()
        
class Form(tk.Frame):
    def __init__(self,root,person=None):
        tk.Frame.__init__(self,root)
        self.root=root
        self.person=person
        self.image=ImageTk.PhotoImage(resizeimage.resize_height(PIL.Image.open(self.person.path),200))
        self.imageLabel=tk.Label(self,image=self.image)
        self.imageLabel.pack()
        self.firstNameField=tk.Entry(self,textvariable=person.firstNameVar)
        self.lastNameField=tk.Entry(self,textvariable=person.lastNameVar)
        self.jobField=tk.Entry(self,textvariable=person.jobVar)
        self.submitButton=tk.Button(self,text="Submit",command=self.submit)
        tk.Label(self,text="First name:").pack()
        self.firstNameField.pack()
        tk.Label(self,text="Last name:").pack()
        self.lastNameField.pack()
        tk.Label(self,text="Job:").pack()
        self.jobField.pack()
        self.submitButton.pack()
        self.bind("<Return>",self.submit)
        self.jobField.bind("<Return>",self.submit)
    def submit(self,event=None):
        self.person.firstName = self.person.firstNameVar.get()
        self.person.lastName = self.person.lastNameVar.get()
        self.person.job=self.person.jobVar.get()
        self.root.submitted()
    def focusOn(self):
        self.pack()
        self.jobField.focus_force()
    def focusOff(self):
        self.pack_forget()
class Person:
    def __init__(self,path):
        self.path=path
        genFirstName,genLastName=self.extractName()
        self.firstNameVar,self.lastNameVar,self.jobVar=tk.StringVar(),tk.StringVar(),tk.StringVar()
        self.firstNameVar.set(genFirstName)
        self.lastNameVar.set(genLastName)
        self.firstName,self.lastName,self.job="","",""
    def extractName(self):
        assert ('/' in self.path)
        assert ('.' in self.path)
        slashIndex = self.path.rfind('/')
        dotIndex = self.path.rfind('.')
        fileName = self.path[slashIndex+1:dotIndex]
        if not "_" in fileName: return [fileName,""]
        else:
            underscoreIndex = fileName.find('_')
            firstName = fileName[:underscoreIndex]
            lastName = fileName[underscoreIndex+1:]
            return [firstName,lastName]
def generateXML(people):
    root=ET.Element('people')
    for person in people:
        identifier = (person.firstName+person.lastName).replace(" ","")
        sub = ET.SubElement(root,identifier)
        firstNameElement=ET.SubElement(sub,'FirstName')
        firstNameElement.text=person.firstName
        lastNameElement=ET.SubElement(sub,'LastName')
        lastNameElement.text=person.lastName
        jobElement=ET.SubElement(sub,'Job')
        jobElement.text=person.job
        pathElement = ET.SubElement(sub,'Path')
        pathElement.text=person.path
        ET.dump(sub)
    pretty = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    return pretty
def createXML(mainWindow=None):
    MainRoot(master=mainWindow)
main = Main()
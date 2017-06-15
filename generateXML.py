import os
import sys
from os import listdir
from os.path import isfile, join
import glob
import tkinter
from tkinter import *
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk
from resizeimage import resizeimage
import xml.etree.ElementTree as ET
import xml.dom.minidom
class MainRoot(Toplevel):
    def __init__(self,*args,**kwargs):
        Toplevel.__init__(self,*args,**kwargs)
        #root=Tk()
        #root.withdraw()
        self.title="tehoi"
        self.paths = self.getPaths()
        self.people = [Person(path) for path in self.paths]
        self.forms = [Form(self,person=person) for person in self.people]
        self.currentForm = 0
        self.forms[self.currentForm].pack()
        mainloop()
    def getPaths(self):
        picturesDirectory = filedialog.askdirectory(initialdir="/", title="Please select the directory of the images")
        #input("Press Enter to continue...")
        dirContents = [picturesDirectory+"/"+file for file in listdir(picturesDirectory)]
        filePaths = [path for path in dirContents if isfile(path)]
        return filePaths
    def submitted(self):
        if self.currentForm==len(self.forms)-1:
            self.quit()
            self.destroy()
        else:
            self.forms[self.currentForm].pack_forget()
            self.currentForm+=1
            self.forms[self.currentForm].pack()
            self.forms[self.currentForm].focus_set()
            self.forms[self.currentForm].jobField.focus_set()
class Form(Frame):
    def __init__(self,root,person=None):
        Frame.__init__(self,root)
        self.root=root
        self.person=person
        self.image=ImageTk.PhotoImage(resizeimage.resize_height(Image.open(self.person.path),200))
        self.imageLabel=Label(self,image=self.image)
        self.imageLabel.pack()
        self.firstNameField=Entry(self,textvariable=person.firstNameVar)
        self.lastNameField=Entry(self,textvariable=person.lastNameVar)
        self.jobField=Entry(self,textvariable=person.jobVar)
        self.submitButton=Button(self,text="Submit",command=self.submit)
        Label(self,text="First name:").pack()
        self.firstNameField.pack()
        Label(self,text="Last name:").pack()
        self.lastNameField.pack()
        Label(self,text="Job:").pack()
        self.jobField.pack()
        #self.jobField.focus_set()
        self.submitButton.pack()
        self.bind("<Return>",self.submit)
        self.jobField.bind("<Return>",self.submit)
    def submit(self,event=None):
        self.person.firstName = self.person.firstNameVar.get()
        self.person.lastName = self.person.lastNameVar.get()
        self.person.job=self.person.jobVar.get()
        self.root.submitted()
class Person:
    def __init__(self,path):
        self.path=path
        genFirstName,genLastName=self.extractName()
        self.firstNameVar,self.lastNameVar,self.jobVar=StringVar(),StringVar(),StringVar()
        self.firstNameVar.set(genFirstName)
        self.lastNameVar.set(genLastName)
        self.firstName,self.lastName,self.job="","",""
    def extractName(self):
        assert ('/' in self.path)
        assert ('.' in self.path)
        slashIndex = self.path.rfind('/')
        dotIndex = self.path.rfind('.')
        fileName = self.path[slashIndex+1:dotIndex]
        if not "_" in fileName: return [filename,""]
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
    #thing1=ET.tostring(root)
    #print(thing1)
    #thing2=xml.dom.minidom.parseString(thing1)
    #thing3=thing2.toprettyxml()
    pretty = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    #pretty_xml = thing.toprettyxml()
    
    file=open('PeopleList.xml','w')
    file.write(pretty)
    file.close()
def xmlCreation():
    mainRoot = MainRoot()
    people = mainRoot.people
    generateXML(people)
def main():
    xmlCreation()
main()
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
class MainRoot:
    def __init__(self):
        #self.master=master
        self.paths = self.getPaths()
        master=Toplevel()
        self.people = [Person(path,master) for path in self.paths]
        self.forms = 
    def getPaths(self):
        picturesDirectory = filedialog.askdirectory(initialdir="/", title="Please select the directory of the images")
        dirContents = [picturesDirectory+"/"+file for file in listdir(picturesDirectory)]
        filePaths = [path for path in dirContents if isfile(path)]
        return filePaths
class Person:
    def __init__(self,picturePath,master):
        self.picturePath=picturePath
        self.firstName,self.lastName = self.extractName()
        self.firstName,self.lastName,self.job=self.askForInfo(master)
        self.image = None
    def extractName(self):
        path = self.picturePath
        assert ('/' in path)
        assert ('.' in path)
        slashIndex = path.rfind('/')
        dotIndex = path.rfind('.')
        fileName = path[slashIndex+1:dotIndex]
        if not "_" in fileName: return [filename,""]
        else:
            underscoreIndex = fileName.find('_')
            firstName = fileName[:underscoreIndex]
            lastName = fileName[underscoreIndex+1:]
            return [firstName,lastName]
    def askForInfo(self,master):
        firstNameVar = StringVar()
        firstNameVar.set(self.firstName)
        lastNameVar = StringVar()
        lastNameVar.set(self.lastName)
        jobVar = StringVar()
        form = Form(self,self.picturePath,firstNameVar,lastNameVar,jobVar,master)
        self.firstName = firstnameVar.get()
        self.lastName = lastNameVar.get()
        self.job = jobVar.get()
        return firstNameVar.get(),lastNameVar.get(),jobVar.get()
    def __str__(self):
        return "First name: "+self.firstName+"\nLast name: "+self.lastName+"\nJob: "+self.job+"\n"
class Form:
    def __init__(self,person,picturePath,firstNameVar,lastNameVar,jobVar,master):
        self.form = Frame(master)
        self.person = person
        self.firstNameVar = firstNameVar
        self.lastNameVar = lastNameVar
        self.jobVar = jobVar
        firstNameField = Entry(self.form,textvariable=firstNameVar)
        lastNameField = Entry(self.form,textvariable=lastNameVar)
        jobField = Entry(self.form,textvariable=jobVar)
        submitButton = Button(self.form,text="Submit",command=self.submit)
        
        self.packImage(picturePath)
        
        Label(self.form,text="First name:").pack()
        firstNameField.pack()
        Label(self.form,text="Last name:").pack()
        lastNameField.pack()
        Label(self.form,text="Job:").pack()
        jobField.pack()
        submitButton.pack()
        #self.form.pack()
        #mainloop()
    def packImage(self,path):
        pilImage = Image.open(path)
        pilImage = resizeimage.resize_height(pilImage,200)
        self.person.image = pilImage
        image=ImageTk.PhotoImage(pilImage)
        label = Label(self.form,image=image)
        label.photo = image
        label.pack()
    def submit(self):
        self.person.firstName = self.firstNameVar
        self.person.lastName = self.lastNameVar
        self.person.job = self.jobVar
        self.master.
        #self.pack_forget()
        #self.form.quit()
        #self.form.destroy()
def generateXML(people):
    root=ET.Element('people')
    for person in people:
        identifier = person.firstName+person.lastName
        sub = ET.SubElement(root,identifier)
        firstNameElement=ET.SubElement(sub,'FirstName')
        firstNameElement.text=person.firstName
        lastNameElement=ET.SubElement(sub,'LastName')
        lastNameElement.text=person.lastName
        jobElement=ET.SubElement(sub,'Job')
        jobElement.text=person.job
        pathElement = ET.SubElement(sub,'Path')
        pathElement.text=person.picturePath
        ET.dump(sub)
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
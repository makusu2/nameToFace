import xml.etree.ElementTree as ET
import os
import tkinter
from tkinter import *
from tkinter import filedialog
def main(mainWindow=None):
    tree=ET.parse(filedialog.askopenfilename(parent=mainWindow,title="Please open the XML file of the employees."))
    root=tree.getroot()
    people = [{'firstName':person.find('FirstName').text,'lastName':person.find('LastName').text,'job':person.find('Job').text,'path':person.find('Path').text} for person in root]
    s="<!DOCTYPE html>\n<html>\n<body>\n"
    for i,person in enumerate(people):
        colNum=i%3
        assert colNum in [0,1,2]
        personName = person['firstName']+" "+person['lastName']
        innerString="\t\t\t\t<img src=\""+person['path']+"\" style=\"width: 250px; height: 250px;\" />\n\t\t\t\t<center>"+personName+"</center>\n\t\t\t\t<center>"+person['job']+"</center>\n\t\t\t\t<p />\n"
        if colNum==0:
            s+="\t<div class=\"row\">\n\t\t<div class=\"col-md-12\">\n\t\t\t<div style=\"float: left; width: 33%;\">\n"
        elif colNum==1:
            s+="\t\t\t<div style=\"float: right; width: 33%;\">\n"
        else:
            s+="\t\t\t<div style=\"display: inline-block; width: 33%;\">\n"
        s+=innerString
        s+="\t\t\t</div>\n"
        if colNum==2 or i==len(people)-1:
            s+="\t\t</div>\n\t</div>\n</body>\n</html>\n"
    file=filedialog.asksaveasfile(master=mainWindow,title="Please enter the name of which the HTML file should be saved")
    file.write(s)
    file.close()
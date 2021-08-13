from string import Template
from inspect import cleandoc
from typing import Union
from collections.abc import Sequence

class Section:
    def __init__(self, title:str, nest:int =0, data=None):
        self.title = "{markdownheading} {title}\n".format(markdownheading = '#'*(nest+1), title=title)
        self.data = ''        
        self.subSections = []
    def addSubSection(self, subsection):
        self.subSections.append(subsection)
    def writeOut(self):
        text = self.title+self.data
        for subsection in self.getSubSections():
            text += subsection.writeOut()
        return text
    def getSubSections(self):
        return (section for section in self.subSections)

class ListSection(Section):
    def __init__(self, title:str, nest:int =1, data=None):
        super().__init__(title,nest)
        if data != None:
            self.data = ''.join('- {}\n'*len(data)).format(*data)

class ValueSection(Section):
    def __init__(self, title: str, nest: int =1, data=None):
        super().__init__(title, nest)
        if data != None:
            self.data = ''.join('{:.2f}\n').format(data)

class GraphicSection(Section):
    def __init__(self, title: str, nest: int=1, data=None):
        super().__init__(title, nest)
        if data != None:
            self.data = "![Graph of roll distributions]({})\n".format(data)

        


class Report:
    def __init__(self):
        self.sections = []

    def addSection(self, section):
        self.sections.append(section)
    
    def export(self, exportPath, fileName):
        with open(exportPath+fileName, 'w') as file:
            for section in self.sections:
                file.write(section.writeOut())
            file.close()
        return exportPath+fileName
                
                
    



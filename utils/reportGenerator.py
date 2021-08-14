from inspect import cleandoc
from datetime import datetime

class Section:
    def __init__(self, title:str=None, nest:int =0, data=None):
        if title != None:
            self.title = "\n{markdownheading} {title}\n".format(markdownheading = '#'*(nest+1), title=title)
        else:
            self.title = ''
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
    def __init__(self, title:str=None, nest:int =1, data=None):
        super().__init__(title,nest)
        if data != None:
            self.data = ''.join('- {}\n'*len(data)).format(*data)

class ValueSection(Section):
    def __init__(self, title: str=None, nest: int =1, data=None):
        super().__init__(title, nest)
        if data != None:
            self.data = ''.join('{:.2f}\n').format(data)

class GraphicSection(Section):
    def __init__(self, title: str=None, nest: int=1, data=None, alttext=None):
        super().__init__(title, nest)
        if data != None:
            self.data = "![{}]({})\n".format(alttext,data)

class Header(Section):
    def __init__(self, title: str= None, nest: int=0, data=None):
        super().__init__(title, nest)
        if data != None:
            self.data = cleandoc("""
                Report Generated: {}\n
                Input File: {}\n
                Logger: {}\n
            """).format(*data)



class Report:
    def __init__(self, logger, file):
        self.sections = []
        headerInfo = [datetime.now().isoformat(), file, logger]
        self.addSection(Header("FFXIV Loot Analyzer",data = headerInfo))

    def addSection(self, section):
        self.sections.append(section)
        return section
    
    def export(self, exportPath, fileName):
        with open(exportPath+fileName, 'w') as file:
            for section in self.sections:
                file.write(section.writeOut())
            file.close()
        return exportPath+fileName
                
                
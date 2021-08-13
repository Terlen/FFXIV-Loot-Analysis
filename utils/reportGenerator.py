from string import Template
from inspect import cleandoc
from typing import Union
from collections.abc import Sequence

class Section:
    
    def __init__(self, title:str, nest:int =0, data=None):
        self.title = "{heading} {title}\n".format(heading = '#'*(nest+1), title=title)
        self.data = ''        
        self.subSections = []
    def addSubSection(self, subsection):
        self.subSections.append(subsection)

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
    

    def loadTemplate(templateDir: str):
        with open(templateDir, 'r') as template:
            format = Template(template.read())
            template.close()
        return format

    def listFormat(iterable : Union[list,set]):
        return ''.join('\n- {}'.format(item) for item in iterable)

    
    def __init__(self, template: str):
        self.template = self.loadTemplate(template)
        self.templateMap = {}
    
def reportBuilder(flags:list):
    header = Section('header', )
    


def reportSave(outfolder, data):
    with open(outfolder+'report.md', 'w') as f:
        f.write(data)
        f.close()
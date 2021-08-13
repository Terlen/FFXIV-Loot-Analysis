from string import Template
from inspect import cleandoc
from typing import Union

def loadTemplate(templateDir: str):
    with open(templateDir, 'r') as template:
        format = Template(template.read())
        template.close()
    return format

def listFormatter(iterable : Union[list,set]):
    return ''.join('\n- {}'.format(item) for item in iterable)

def reportBuilder(filename:str, logger:str, members:set, template: Template):
    templateMap = {}
    templateMap['file'] = filename
    templateMap['logger'] = logger
    templateMap['members'] = listFormatter(members)
    return template.substitute(templateMap)


def reportSave(outfolder, data):
    with open(outfolder+'report.md', 'w') as f:
        f.write(data)
        f.close()
'''
Test for operation lowercase
-- instead of using expression
but the actual changes
'''
# Backwards Compatible Reproducible OR
import json
from collections import OrderedDict
from itertools import product

import OpenRefineOperations as OR

def GetColumnName(projectID):
    response=OR.get_models(projectID)
    column_model = response['columnModel']
    column_name = [column['name'] for column in column_model['columns']]
    return column_name



def returnEdit(fromcelllist, tocelllist):
    # edit:[{'from':{}, 'to':}]
    edit=[{'from':f1, 'to':t} for f1,t in zip(fromcelllist, tocelllist)]
    return edit




project_id=OR.create_project('Dataset/HalfMenu.csv','BC_test2')

log_file=[]
changes=OrderedDict()
# Input column name: 'sponsor'
# Return column index
columnIndex=GetColumnName(project_id).index('sponsor')

# Before the operation
fromvalue=OR.get_cell_value(project_id,columnIndex)
print('from values:',fromvalue)

# do operation : Lowercase
OR.text_transform(project_id,'sponsor','value.toLowercase()')

# after the operation
tovalue=OR.get_cell_value(project_id,columnIndex)
print('to values:',tovalue)

Edits=returnEdit(fromvalue,tovalue)
changes['changes']=Edits
log_file.append(changes)
with open('add_on.json','wt')as f:
    json.dump(log_file,f,indent=2)



'''

[
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column sponsor using expression value.replace(\"super\",\"supper\")",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "sponsor",
    "expression": "value.replace(/supper menu, s\\. s\\. vaderland, march 18th, 1910\\./i,\"super\")",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10
  }
]
'''

# backwards

for to_cell,from_cell in zip(tovalue,fromvalue):
    try:
        OR.text_transform(project_id,'sponsor','value.replace("%s","%s")'%(to_cell['v'],from_cell['v']))
    except:
        pass




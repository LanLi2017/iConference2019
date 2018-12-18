import json
from pprint import pprint


__author__='Lan Li'
# create
import OpenRefineOperations as OR


def main():
    project_Name=raw_input('Enter the project name:\n')
    project_path=OR.input_path_convenient('Enter the input dataset path:\n')
    JSON_path=OR.input_path_convenient('Enter the input OR_JSON path:\n')
    projectID=OR.create_project(project_path,project_Name)

    '''     
    Enhanced(original+compute_clusters[type, method, function])
    '''
    with open(JSON_path,'r')as f:
        dataset=json.load(f)

    for dicts in dataset:
        if dicts['op']=='core/column-rename':
            oldcol=dicts['oldColumnName']
            newcol=dicts['newColumnName']
            OR.rename_column(projectID,oldcol,newcol)
        elif dicts['op']=='core/mass-edit':
            columnName=dicts['columnName']
            clusterer_type=dicts['Cluster-type']
            function=dicts['Cluster-function']
            try:
                params=dicts['Cluster-params']
                compute_clusters=OR.compute_clusters(projectID,columnName,clusterer_type=clusterer_type,function=function,params=params)
            except KeyError:
                compute_clusters=OR.compute_clusters(projectID,columnName,clusterer_type=clusterer_type,function=function)
            Edit_from=OR.getFromValue(compute_clusters)
            Edit_to=OR.getToValue(compute_clusters)
            edits=[{'from':f1, 'to':t} for f1,t in zip(Edit_from, Edit_to)]
            OR.mass_edit(projectID,columnName,edits)

        elif dicts['op']=='core/text-transform':
            columnName=dicts['columnName']
            expression=dicts['expression']
            OR.text_transform(projectID,columnName,expression)
        elif dicts['op']=='core/column-split':
            columnName=dicts['columnName']
            separator=dicts['separator']
            OR.split_column(projectID,columnName,separator)
        elif dicts['op']=='single-edit':
            optype=dicts['type']
            oprowIndex=dicts['rowIndex']
            opcellIndex=dicts['cellIndex']
            opnew=dicts['new']
            OR.single_edit(projectID,oprowIndex,opcellIndex,optype,opnew)

        elif dicts['op']=='star-row':
            oprowIndex=dicts['rowIndex']
            OR.star_row(projectID,oprowIndex)
    with open('OutputDataset/%s.csv'%project_Name, 'wb')as f:
        f.writelines(OR.export(projectID,'csv'))


if __name__=='__main__':
    main()




# coding=utf-8
import csv
import json

# import sys
# sys.path.append('/Users/barbaralee/WT-summer-2018-Lan-Li/OpenRefine3Operations/Menu_case/Python_command/Openrefine-client reproducible json/script')
import os
from pprint import pprint

import OpenRefineOperations as OR

import subprocess


# get yes or no to continue
def Confirm(message,default=None):
    while True:
        if default is None:
            message += ' (y/n)'
        elif default:
            # set Yes as default
            message += ' (Y/n)'
        else:
            # set No as default
            message += ' (y/N)'

        input_str=raw_input(message).lower()
        # if no input :
        if default is not None and not input_str:
            return default
        elif input_str == 'y':
            return True
        elif input_str == 'n':
            return False


def prompt_int(message, min=None, max=None):
    while True:
        input_str = raw_input(message)

        try:
            value = int(input_str)

            if min is not None and value < min:
                raise ValueError
            if max is not None and value > max:
                raise ValueError

        except ValueError:
            pass
        else:
            return value


# Choice with corresponding index
def prompt_options(options):
    for idx, option in enumerate(options, start=1):
        print(idx, option)

    if not options:
        return 0
    else:
        return prompt_int('Please enter your choice: ', min=1, max=len(options))


def GetColumnName(projectID):
    response=OR.get_models(projectID)
    column_model = response['columnModel']
    column_name = [column['name'] for column in column_model['columns']]
    return column_name

def CheckColumnName(op,projectid):
    columnnamelist=GetColumnName(projectid)
    print('column name list : {}\n'.format(columnnamelist))
    while True:
        userrenamechoice=raw_input("Enter the column name you want to do {},"
                                   "if there is no other columns you want to make change, enter N: ".format(op))
        if userrenamechoice in columnnamelist or userrenamechoice.lower()=='n':
            return userrenamechoice
        else:
            print("column name not found, please re-enter: ")


def main():
    result=[]
    print("Welcome to use OpenRefine userScript")
    # import project
    while True:
        choice=prompt_options([
            'List Projects',
            'Create Project',
            'Get Project Name',
            'Exit',
        ])
        if choice==1:
            project_id=OR.list_objects()
            pprint(project_id)
        elif choice==3:
            project_id_list=OR.get_project_id()
            pprint(project_id_list)
            usergetprojectID=raw_input("input the project ID:")
            projectname=OR.get_project_name(usergetprojectID)
            print(projectname)
            # f.write('Get Project Name')
        elif choice==2:
            userinputpath=OR.input_path_convenient('please input CSV name:')
            userinputname=raw_input('please input new project name:')
            projectID=OR.create_project(userinputpath,userinputname)

            number_rows=raw_input("Display some number of rows: You can choose 5/10/25/50")
            print("Show the first "+number_rows+" rows for this project:")

            with open(userinputpath,'rb') as project:
                content=tuple(project)
                header=content[0]
                print(header)
                # data=tuple(content[1:int(number_rows)+1])
                for i in range(1,int(number_rows)+1):
                    print(content[i])
            userrenamechoice=CheckColumnName('rename',projectID)
            while userrenamechoice.lower()!='n':
                renamedicts={}
                renamedicts['op']='core/column-rename'
                newcolumnname=raw_input("Enter the new column name:")
                renamedicts['description']='Rename column %s to %s'%(userrenamechoice, newcolumnname)
                renamedicts['oldColumnName']='%s'%userrenamechoice
                renamedicts['newColumnName']='%s'%newcolumnname
                result.append(renamedicts)
                OR.rename_column(projectID,userrenamechoice,newcolumnname)
                userrenamechoice=CheckColumnName('rename',projectID)

            # further operations
            usercolumn=CheckColumnName('Data Cleaning',projectID)
            while usercolumn.lower()!='n':
                while True:
                    userOperates=prompt_options([
                        'Cluster and Relabel',
                        'Trim Whitespace',
                        'Lowercase the column value',
                        'Uppercase the column value',
                        'Transform the column value to Date',
                        'Transform the column value to Numeric',
                        'Split multi-valued cells in column ',
                        'Single Edit cell',
                        'star this row',
                        'Exit this column',
                    ])
                    if userOperates==1:
                        ClusterRelabeldicts={}
                        ClusterRelabeldicts['op']='core/mass-edit'
                        ClusterRelabeldicts['description']='Mass edit cells in column %s'%usercolumn
                        ClusterRelabeldicts['engineConfig']={}
                        ClusterRelabeldicts['engineConfig']['mode']='row-based'
                        ClusterRelabeldicts['engineConfig']['facets']='[]'
                        ClusterRelabeldicts['columnName']='%s'%usercolumn
                        ClusterRelabeldicts['expression']='value'

                        # print("please choose clustering type:")
                        print("1. binning")
                        print("2. knn")
                        userClusterer=raw_input("please choose clustering type:")
                        if userClusterer=='1':
                            ClusterRelabeldicts['Cluster-type']='binning'
                            userFunction=prompt_options([
                                'fingerprint',
                                'ngram-fingerprint',
                                'metaphone3',
                                'cologne-phonetic',
                            ])
                            if userFunction==1:
                                ClusterRelabeldicts['Cluster-function']='fingerprint'
                                result.append(ClusterRelabeldicts)
                                compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='fingerprint')
                            elif userFunction==2:
                                ClusterRelabeldicts['Cluster-function']='ngram-fingerprint'
                                params=raw_input("Enter the params for Ngram size:")
                                ClusterRelabeldicts['Cluster-params']='%s'%params
                                result.append(ClusterRelabeldicts)
                                compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='ngram-fingerprint',params=params)
                            elif userFunction==3:
                                ClusterRelabeldicts['Cluster-function']='metaphone3'
                                result.append(ClusterRelabeldicts)
                                compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='metaphone3')
                            elif userFunction==4:
                                ClusterRelabeldicts['Cluster-function']='cologne-phonetic'
                                result.append(ClusterRelabeldicts)
                                compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='cologne-phonetic')

                        elif userClusterer=='2':
                            ClusterRelabeldicts['Cluster-type']='knn'
                            userKNNfunction=prompt_options([
                               'levenshtein',
                               'PPM',
                            ])
                            if userKNNfunction==1:
                                ClusterRelabeldicts['Cluster-function']='levenshtein'
                                print("Please set the params: ")
                                userinputradius=float(raw_input("Set the radius: "))
                                userinputNgramsize=int(raw_input("Set the Bloking Ngram-size: "))
                                ClusterRelabeldicts['Cluster-params']='{"radius":%f, "blocking-ngram-size":%d}'%(userinputradius,userinputNgramsize)
                                result.append(ClusterRelabeldicts)
                                compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type='knn',function='levenshtein',params={ 'radius':userinputradius,'blocking-ngram-size':userinputNgramsize})
                            elif userKNNfunction==2:
                                ClusterRelabeldicts['Cluster-function']='PPM'
                                print("Please set the params: ")
                                userinputradius=float(raw_input("Set the radius: "))
                                userinputNgramsize=int(raw_input("Set the Bloking Ngram-size: "))
                                ClusterRelabeldicts['Cluster-params']='{"radius":%f, "blocking-ngram-size":%d}'%(userinputradius,userinputNgramsize)
                                result.append(ClusterRelabeldicts)
                                compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type='knn',function='PPM',params={ 'radius':userinputradius,'blocking-ngram-size':userinputNgramsize})
                        print(compute_clusters)
                        userClusterinput=raw_input("Do you want to do manually edition for cluster? If not, input N; else input Y: ")

                        Edit_from=OR.getFromValue(compute_clusters)
                        Edit_to=OR.getToValue(compute_clusters)
                        if userClusterinput =='N':
                            edits=[{'from':f1, 'to':t} for f1,t in zip(Edit_from, Edit_to)]
                            print(edits)
                            ClusterRelabeldicts['edits']=edits
                            OR.mass_edit(projectID,usercolumn,edits,expression='value')
                        elif userClusterinput=='Y':
                            print("This is the original values in cluster: ")
                            print(Edit_from)
                            print("This is the values after the chosen cluster: ")
                            print(Edit_to)
                            Edit_new_to=[]
                            for to in Edit_to:
                                print(to)
                                userinputTo=raw_input("Input the value you want to make change with this value, if not, input N")
                                if userinputTo!='N':

                                    to=userinputTo
                                    Edit_new_to.append(to)
                                else:
                                    to=to
                                    Edit_new_to.append(to)
                            print(Edit_new_to)
                            mannually_edits=[{'from':f1, 'to':t} for f1,t in zip(Edit_from, Edit_new_to)]
                            ClusterRelabeldicts['edits']=mannually_edits
                            OR.mass_edit(projectID,usercolumn,mannually_edits,expression='value')

                    elif userOperates==2:
                        trimdicts={}
                        trimdicts['op']='core/text-transform'
                        trimdicts['description']='Text transform on cells in column %s using expression value.trim()'%usercolumn
                        trimdicts['engineConfig']={}
                        trimdicts['engineConfig']['mode']='row-based'
                        trimdicts['engineConfig']['facets']='[]'
                        trimdicts['columnName']='%s'%usercolumn
                        trimdicts['expression']='value.trim()'
                        trimdicts['onError']='set-to-blank'
                        trimdicts['repeat']='false'
                        trimdicts['repeatCount']=10
                        result.append(trimdicts)

                        OR.text_transform(projectID,usercolumn,'value.trim()')
                    elif userOperates==3:
                        Lowercasedicts={}
                        Lowercasedicts['op']='core/text-transform'
                        Lowercasedicts['description']='Text transform on cells in column %s using expression value.toLowercase()'%usercolumn
                        Lowercasedicts['engineConfig']={}
                        Lowercasedicts['engineConfig']['mode']='row-based'
                        Lowercasedicts['engineConfig']['facets']='[]'
                        Lowercasedicts['columnName']='%s'%usercolumn
                        Lowercasedicts['expression']='value.toLowercase()'
                        Lowercasedicts['onError']='set-to-blank'
                        Lowercasedicts['repeat']='false'
                        Lowercasedicts['repeatCount']=10
                        result.append(Lowercasedicts)
                        OR.text_transform(projectID,usercolumn,'value.toLowercase()')
                    elif userOperates==4:

                        Uppercasedicts={}
                        Uppercasedicts['op']='core/text-transform'
                        Uppercasedicts['description']='Text transform on cells in column %s using expression value.toUppercase()'%usercolumn
                        Uppercasedicts['engineConfig']={}
                        Uppercasedicts['engineConfig']['mode']='row-based'
                        Uppercasedicts['engineConfig']['facets']='[]'
                        Uppercasedicts['columnName']='%s'%usercolumn
                        Uppercasedicts['expression']='value.toUppercase()'
                        Uppercasedicts['onError']='set-to-blank'
                        Uppercasedicts['repeat']='false'
                        Uppercasedicts['repeatCount']=10
                        result.append(Uppercasedicts)

                        OR.text_transform(projectID,usercolumn,'value.toUppercase()')
                    elif userOperates==5:
                        Datedicts={}
                        Datedicts['op']='core/text-transform'
                        Datedicts['description']='Text transform on cells in column %s using expression value.toDate()'%usercolumn
                        Datedicts['engineConfig']={}
                        Datedicts['engineConfig']['mode']='row-based'
                        Datedicts['engineConfig']['facets']='[]'
                        Datedicts['columnName']='%s'%usercolumn
                        Datedicts['expression']='value.toDate()'
                        Datedicts['onError']='set-to-blank'
                        Datedicts['repeat']='false'
                        Datedicts['repeatCount']=10
                        result.append(Datedicts)

                        OR.text_transform(projectID,usercolumn,'value.toDate()')
                    elif userOperates==6:
                        Numberdicts={}
                        Numberdicts['op']='core/text-transform'
                        Numberdicts['description']='Text transform on cells in column %s using expression value.toNumber()'%usercolumn
                        Numberdicts['engineConfig']={}
                        Numberdicts['engineConfig']['mode']='row-based'
                        Numberdicts['engineConfig']['facets']='[]'
                        Numberdicts['columnName']='%s'%usercolumn
                        Numberdicts['expression']='value.toNumber()'
                        Numberdicts['onError']='set-to-blank'
                        Numberdicts['repeat']='false'
                        Numberdicts['repeatCount']=10
                        result.append(Numberdicts)

                        OR.text_transform(projectID,usercolumn,'value.toNumber()')
                    elif userOperates==7:
                        Splitdicts={}
                        Splitdicts['op']='core/column-split'
                        Splitdicts['description']='Split column %s by separator'%usercolumn
                        Splitdicts['engineConfig']={}
                        Splitdicts['engineConfig']['mode']='row-based'
                        Splitdicts['engineConfig']['facets']='[]'
                        Splitdicts['columnName']='%s'%usercolumn
                        Splitdicts['guessCellType']='true'
                        usersetremove=raw_input("Remove the original column or not,set true or false")
                        Splitdicts['removeOriginalColumn']='%s'%usersetremove
                        Splitdicts['mode']='separator'

                        userSeparator=raw_input("input the separator: ")
                        Splitdicts['separator']='%s'%userSeparator
                        Splitdicts['regex']='false'
                        Splitdicts['maxColumns']=0
                        result.append(Splitdicts)
                        OR.split_column(projectID,usercolumn,userSeparator,remove_original_column=usersetremove)
                        # something special here
                        # if split into several columns, then usercolumn will change
                    elif userOperates==8:
                        Onedicts={}
                        Onedicts['op']='single-edit'
                        userrowindex=int(raw_input('input the row number for edits, row number starts from 0:'))
                        usercellindex=int(raw_input('input the column number for edits:'))
                        # get the original cell
                        usernewcell=raw_input('input the new cell:')
                        '''
                        type choice:
                        number
                        boolean
                        date
                        default=String
                        '''
                        usertype=raw_input('input the value type:')
                        Onedicts['description']='Edit single cell on row %s, column %s'%(userrowindex,usercolumn)
                        Onedicts['columnName']='%s'%usercolumn
                        Onedicts['rowIndex']=userrowindex
                        Onedicts['cellIndex']=usercellindex
                        Onedicts['type']=usertype
                        Onedicts['new']=usernewcell
                        result.append(Onedicts)

                        OR.single_edit(projectID,userrowindex,usercellindex,usertype,usernewcell)
                    elif userOperates==9:
                        stardicts={}
                        stardicts['op']='star-row'
                        rowindex=int(raw_input('input the row number, row number starts from 0:'))
                        stardicts['rowIndex']=rowindex
                        result.append(stardicts)
                        OR.star_row(projectID,rowindex,starred=True)
                    elif userOperates==10:
                        if Confirm("Are you sure to stop doing Data Wrangling?",default=False):
                            break
                usercolumn=CheckColumnName('Data Cleaning',projectID)
        elif choice==4:
            if Confirm("Are you sure to exit?",default=False):
                with open('Enhanced_JSON/EnhancedRecipe.json','wt')as f:
                    json.dump(result,f,indent=2)
                break


if __name__=='__main__':
    main()













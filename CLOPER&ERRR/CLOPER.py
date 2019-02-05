# coding=utf-8
import csv
import json

# import sys
# sys.path.append('/Users/barbaralee/WT-summer-2018-Lan-Li/OpenRefine3Operations/Menu_case/Python_command/Openrefine-client reproducible json/script')
import os
from collections import OrderedDict
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


def GetColumnLength(projectID):
    response=OR.get_models(projectID)
    column_model = response['columnModel']
    column_name = [column['name'] for column in column_model['columns']]
    return len(column_name)-1


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


def returnEdit(fromcelllist, tocelllist):
    # edit:[{'from':{}, 'to':}]
    edit=[{'from':f1, 'to':t} for f1,t in zip(fromcelllist, tocelllist)]
    return edit

def returnchanges(counterlist, valuelist):
    changes=[{'counter': c1, 'value': v1} for c1,v1 in zip(counterlist,valuelist)]
    return changes


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
            opindex=0
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
                renamedicts=OrderedDict()
                renamedicts['op']='core/column-rename'
                newcolumnname=raw_input("Enter the new column name:")
                renamedicts['description']='Rename column %s to %s'%(userrenamechoice, newcolumnname)
                renamedicts['oldColumnName']='%s'%userrenamechoice
                renamedicts['newColumnName']='%s'%newcolumnname
                OR.rename_column(projectID,userrenamechoice,newcolumnname)
                # retrospective description after the operation
                No_changes=OR.returnRetro_Description(projectID,opindex)
                renamedicts['changes']='%s'%No_changes
                result.append(renamedicts)
                opindex+=1
                userrenamechoice=CheckColumnName('rename',projectID)

            # further operations
            usercolumn=CheckColumnName('Data Cleaning',projectID)
            column_length=GetColumnLength(projectID)
            print('this is the table length:%s'%column_length)

            while usercolumn.lower()!='n':
                columnIndex=GetColumnName(projectID).index(usercolumn)
                while True:
                    userOperates=prompt_options([
                        'Cluster and Edit',
                        'Common transforms',
                        'Split multi-valued cells in column ',
                        'Single Edit cell',
                        'star the row',
                        'Exit this column',
                    ])
                    if userOperates==1:
                        ClusterRelabeldicts=OrderedDict()
                        ClusterRelabeldicts['op']='core/mass-edit'
                        ClusterRelabeldicts['description']='Mass edit cells in column %s'%usercolumn
                        ClusterRelabeldicts['engineConfig']={}
                        ClusterRelabeldicts['engineConfig']['mode']='row-based'
                        ClusterRelabeldicts['engineConfig']['facets']=[]
                        ClusterRelabeldicts['columnName']='%s'%usercolumn
                        ClusterRelabeldicts['expression']='value'

                        # print("please choose clustering type:")
                        cluster_info=[]
                        cluster_type=['binning','knn',]
                        userClusterer=prompt_options(cluster_type)
                        cluster_info.append(cluster_type[userClusterer-1])
                        if userClusterer==1:
                            cluster_function=[
                                'fingerprint',
                                'ngram-fingerprint',
                                'metaphone3',
                                'cologne-phonetic',
                            ]
                            userFunction=prompt_options(cluster_function)
                            cluster_info.append(cluster_function[userFunction-1])
                            if userFunction==2:
                                ngram_size=raw_input("Enter the params for Ngram size:")
                                params={'ngram-size':ngram_size}
                                cluster_info.append(params)
                                compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type=cluster_type[userClusterer-1],function=cluster_function[userFunction-1],params=params)
                            else:
                                compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type=cluster_type[userClusterer-1],function=cluster_function[userFunction-1])

                        elif userClusterer==2:
                            cluster_function=[
                               'levenshtein',
                               'PPM',
                            ]
                            userKNNfunction=prompt_options(cluster_function)
                            cluster_info.append(cluster_function[userKNNfunction-1])
                            print("Please set the params: ")
                            userinputradius=float(raw_input("Set the radius: "))
                            userinputNgramsize=int(raw_input("Set the Bloking Ngram-size: "))
                            params='{"radius":%f, "blocking-ngram-size":%d}'%(userinputradius,userinputNgramsize)
                            cluster_info.append(params)
                            compute_clusters=OR.compute_clusters(projectID,usercolumn,clusterer_type=cluster_type[userClusterer-1],function=cluster_function[userKNNfunction-1],params={ 'radius':userinputradius,'blocking-ngram-size':userinputNgramsize})
                        print(compute_clusters)
                        userClusterinput=raw_input("Do you want to do manually edition for cluster? If not, input N; else input Y: ")

                        Edit_from=OR.getFromValue(compute_clusters)
                        Edit_to=OR.getToValue(compute_clusters)
                        inneredits=OrderedDict()
                        inneredits['fromBlank']='false'
                        inneredits['fromError']='false'
                        if userClusterinput.lower() =='n':
                            for f1,t in zip(Edit_from,Edit_to):
                                inneredits['from']=f1
                                inneredits['to']=t
                            edits=[inneredits]
                            print(edits)
                            ClusterRelabeldicts['edits']=edits
                            OR.mass_edit(projectID,usercolumn,edits,expression='value')
                        elif userClusterinput.lower()=='y':
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

                            for f1,t in zip(Edit_from,Edit_new_to):
                                inneredits['from']=f1
                                inneredits['to']=t
                            mannually_edits=[inneredits]
                            ClusterRelabeldicts['edits']=mannually_edits

                            OR.mass_edit(projectID,usercolumn,mannually_edits,expression='value')
                        #  cluster_info
                        ClusterRelabeldicts['cluster-info']={}
                        ClusterRelabeldicts['cluster-info']['Cluster-type']=cluster_info[0]
                        ClusterRelabeldicts['cluster-info']['Cluster-function']=cluster_info[1]
                        if len(cluster_info)==3:
                            ClusterRelabeldicts['cluster-info']['Cluster-params']=cluster_info[2]
                        # retrospective provenance
                        print("here is the opindex:%s"%opindex)
                        No_changes=OR.returnRetro_Description(projectID,opindex)
                        print(No_changes)
                        ClusterRelabeldicts['changes']='%s'%No_changes
                        result.append(ClusterRelabeldicts)
                        opindex+=1


                    elif userOperates==2:
                        while True:
                            text_expression=[
                                'Trim leading and trailing whitespace',
                                'Collapse consecutive whitespace',
                                'Unescape HTML entities',
                                'To titlecase',
                                'To uppercase',
                                'To lowercase',
                                'To number',
                                'To date',
                                'To text',
                                'Blank out cells',
                                'exit',
                            ]
                            userchoice=prompt_options(text_expression)
                            text_transform=OrderedDict()
                            text_transform['op']='core/text-transform'
                            text_transform['description']='Text transform on cells in column %s using expression %s'%(usercolumn,text_expression[userchoice-1])
                            text_transform['engineConfig']={}
                            text_transform['engineConfig']['mode']='row-based'
                            text_transform['engineConfig']['facets']=[]
                            text_transform['columnName']='%s'%usercolumn
                            fromlist = OR.get_cell_value(projectID,columnIndex)
                            if userchoice==1:
                                text_transform['expression']='value.trim()'
                                # 'from': get_cell_value(), 'to': get_cell_value()
                            elif userchoice==2:
                                text_transform['expression']='value.replace(/\\s+/,' ')'
                            elif userchoice==3:
                                text_transform['expression']='value.unescape("html")'
                            elif userchoice==4:
                                text_transform['expression']='value.toTitlecase()'
                            elif userchoice==5:
                                text_transform['expression']='value.toUppercase()'
                            elif userchoice==6:
                                text_transform['expression']='value.toLowercase()'
                            elif userchoice==7:
                                text_transform['expression']='value.toNumber()'
                            elif userchoice==8:
                                text_transform['expression']='value.toDate()'
                            elif userchoice==9:
                                text_transform['expression']='value.toString()'
                            elif userchoice==10:
                                text_transform['expression']='null'
                            elif userchoice==11:
                                if Confirm("Are you sure to stop doing Data Wrangling?",default=False):
                                    break

                            text_transform['onError']='set-to-blank'
                            text_transform['repeat']='false'
                            text_transform['repeatCount']=10
                            # do operation text_transform
                            OR.text_transform(projectID,usercolumn,text_transform['expression'])
                            tolist=OR.get_cell_value(projectID,columnIndex)
                            text_transform['edit']=returnEdit(fromlist,tolist)
                            pprint(text_transform['edit'])
                            print('here the operation index:%s'%opindex)
                            No_changes=OR.returnRetro_Description(projectID,opindex)
                            text_transform['changes']='%s'%No_changes
                            opindex+=1
                            result.append(text_transform)


                    elif userOperates==3:
                        Splitdicts=OrderedDict()
                        Splitdicts['op']='core/column-split'
                        Splitdicts['description']='Split column %s by separator'%usercolumn
                        Splitdicts['engineConfig']={}
                        Splitdicts['engineConfig']['mode']='row-based'
                        Splitdicts['engineConfig']['facets']=[]
                        Splitdicts['columnName']='%s'%usercolumn
                        Splitdicts['guessCellType']='true'
                        usersetremove=raw_input("Remove the original column or not,set true or false")
                        Splitdicts['removeOriginalColumn']='%s'%usersetremove
                        Splitdicts['mode']='separator'

                        userSeparator=raw_input("input the separator: ")
                        Splitdicts['separator']='%s'%userSeparator
                        Splitdicts['regex']='false'
                        Splitdicts['maxColumns']=0
                        original_columns=GetColumnName(projectID)
                        # do operation
                        OR.split_column(projectID,usercolumn,userSeparator,remove_original_column=usersetremove)
                        # retrospective
                        current_columns=GetColumnName(projectID)
                        diff_columns=filter(lambda x: x not in original_columns,current_columns)
                        Splitdicts['new columns']='%s'%diff_columns
                        number_col_changes=OR.get_split_cell_value(projectID,column_length)[0]
                        act_col_changes=OR.get_split_cell_value(projectID,column_length)[1]
                        Splitdicts['new columns']=returnchanges(number_col_changes,act_col_changes)
                        No_changes=OR.returnRetro_Description(projectID,opindex)
                        Splitdicts['changes']='%s'%No_changes
                        result.append(Splitdicts)
                        opindex+=1
                        # something special here
                        # if split into several columns, then usercolumn will change
                    elif userOperates==4:
                        Onedicts=OrderedDict()
                        Onedicts['op']='single-edit'
                        userrowindex=int(raw_input('input the row number for edits, row number starts from 0:'))
                        usercellindex=int(raw_input('input the column number for edits:'))
                        # get the original cell
                        useroldcell=OR.get_single_cell_value(projectID,usercellindex,userrowindex)
                        usernewcell=raw_input('input the new cell:')
                        edit=[{'from': useroldcell, 'to':usernewcell}]
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
                        Onedicts['edit']=edit
                        # do operation
                        OR.single_edit(projectID,userrowindex,usercellindex,usertype,usernewcell)

                        # retrospective provenance
                        No_changes=OR.returnRetro_Description(projectID,opindex)
                        Onedicts['changes']='%s'%No_changes
                        result.append(Onedicts)
                        opindex+=1
                    elif userOperates==5:
                        stardicts=OrderedDict()
                        stardicts['op']='star-row'
                        stardicts['description']='Star this row'
                        rowindex=int(raw_input('input the row number, row number starts from 0:'))
                        stardicts['rowIndex']=rowindex
                        OR.star_row(projectID,rowindex,starred=True)

                        # retrospective provenance
                        No_changes=OR.returnRetro_Description(projectID,opindex)
                        stardicts['changes']='%s'%No_changes
                        result.append(stardicts)
                        opindex+=1
                    elif userOperates==6:
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













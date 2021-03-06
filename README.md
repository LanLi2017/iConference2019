iConference2019 
================

### Towards More Reproducible Data Wrangling with OpenRefine


Overview
========

OpenRefine (OR) is a popular data wrangling tool. During data cleaning , not only a processed dataset will be generated but also some other provenance-related byproducts. One of them is a native OR recipe (JSON file), and the other one is the Operation History (OH) that lists a series of human-readable data cleaning steps, both of which promote research transparency to some extent by containing some (but incomplete) prospective provenance and partial retrospective provenance information <sup>1</sup>, making them difficult to be directly used for reuse and Reproducibility from OpenRefine Web API. In this poster, a prototype consisting of two sub-systems, one of which extends the native OR recipe to generate a complete recipe (a.k.a. enhanced receipt)  followed by the second re-runner system, is created to complement the missing information between the actual data cleaning operations and the native OR recipe, which meanwhile facilitates transparency, reproducibility and reusability.

<p align="center">
     <img src="https://github.com/LanLi2017/iConference2019/blob/master/README/PNG/DC.png" title="Fig 3.CLOPER" width="600" height="400"/>
</p>


Prototype
=========
The prototype includes two sub-systems. 

1.Command-Line OpenRefine Prototype for Enhanced Recipe （CLOPER）
-------

CLOPER aims to enhance transparency and reusability of the native OR recipe, which reads in the original "messy" dataset (`d1.csv`) and communicates with an OR server through the interface provided by the OR-client. The outputs consist of three products: an enhanced recipe (`EnhancedRecipe.JSON`) is generated at the back-end; a "cleaned" dataet (`d2.csv`) and a native OR recipe (`NativeORRecipe.JSON`) are exported from the OR web UI. 

<p align="center">
     <img src="https://github.com/LanLi2017/iConference2019/blob/master/README/PNG/CLOPER.png" title="Fig 3.CLOPER" width="450" height="400"/>
</p>

2.Enhanced Recipe Re-Runner (ERRR)
----

In regards to reproducibility, ERRR re-implements the enhanced recipe (EnhancedRecipe.JSON) that is derived from CLOPER, applies to the same original "messy" dataset (`d1.csv`). Again ERRR connects to an OR server via OR-client and obtains the same output (`d2.csv`) associated with the native OR recipe (`NativeORRecipe.JSON`).

<p align="center">
     <img src="https://github.com/LanLi2017/iConference2019/blob/master/README/PNG/ERRR.png" width="450" height="400"/>
</p>

Run prototype on your own computer
====


To take advantage of all of the sub-systems in the prototype, you need install the software on your computer

1.Check installed version of Python
---

This prototype requires Python version 2.7. To determine the version of Python installed on your computer use the version option to the python command. For example,


     $ python 
      Python 2.7.10 (default, Jul 15 2017, 17:16:57) 
      [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)] on darwin
      Type "help", "copyright", "credits" or "license" for more information.
      >>>
      
Instructions for installing Python may be found at **[Python Download Website](https://www.python.org/downloads/)**.

2.Project directory layout
----
The directories and the descriptions are listed below:

Directory                             | Description
--------------------------------------|-----------
OR_Client_Library                     | The OpenRefine Python Client Library provides an interface to communicating with an [OpenRefine](http://openrefine.org/) server.
CLOPER&ERRR/Dataset                   | Input "messy" dataset csv file.
CLOPER&ERRR/Enhanced_JSON             | Enhanced Recipe generated by CLOPER system.
CLOPER&ERRR/OR_JSON                   | Native OR Recipe generated by OpenRefine server.
CLOPER&ERRR/OutputDataset             | Ouput "clean(ed)" dataset aftering running enhanced recipe.
CLOPER&ERRR/CLOPER.py                 | Command Line OpenRefine Prototype for Enhanced Recipe.
CLOPER&ERRR/ERRR.py                   | Enhanced Recipe Re-Runner.
CLOPER&ERRR/OpenRefineOperations.py   | Communicate with OR-client library and provides a list of operations to CLOPER and ERRR.
CLOPER&ERRR/Reproducibility.sh        | Bash file for testing the reproducibility of ERRR
README/PNG                            | Figures in Readme.md
   

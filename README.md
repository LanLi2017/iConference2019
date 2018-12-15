iConference2019
===============

# Towards More Reproducible Data Wrangling with OpenRefine

Overview
========


Prototype
=========



Run prototype on your own computer
----------------------------------

To take advantage of all of the sub-systems in the prototype, you need install the software on your computer

### 1. Check installed version of Python

This prototype requires Python version 2.7. To determine the version of Python installed on your computer use the version option to the python command. For example,


     $ python 
      Python 2.7.10 (default, Jul 15 2017, 17:16:57) 
      [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)] on darwin
      Type "help", "copyright", "credits" or "license" for more information.
      >>>
      
Instructions for installing Python may be found at [https://www.python.org/downloads/].

### 2. Project directory layout

The directories and the descriptions are listed below:

Directory            | Description
---------------------|-----------
OR_Client_Library    | The OpenRefine Python Client Library provides an interface to communicating with an `OpenRefine        <http://openrefine.org/>`_ server.
src/main/resources   | Resource files to be packaged with production code.
src/test/java        | Source code for unit and functional tests. Not included in packaged distributions.
src/test/resources   | Resource files available to tests. Not included in packaged distributions.
target               | Destination directory for packaged distributions (jar files) built by maven.
target/classes       | Compiled java classes for source code found under src/main/java.
target/test-classes  | Compiled java classes for test code found under src/test/java.
target/dependency    | Automatically resolved and downloaded dependencies (jars) that will be included in the standalone distribution.
target/site/apidocs/ | Local build of Javadoc documentation.

   

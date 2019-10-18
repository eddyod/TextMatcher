Configuration of Project Environment
*************************************

This is a python module that matches text from a database table. It is useful when you allowed your users to enter text that gets
redundant. It uses python3, Fuzzywuzzy, mysql, pydboc and other libraries.

Overview on how to run this module
================================
1. Install a Python virtualenv
2. Install packages required
3. Have access to the mysql or MS sql server
4. Have access to a linux server that can access the databases

Setup procedure
================

A. Configure
------------------------------------------------------------------------------------------------

1. Create a Python Virtual Environment
    - Make the dir if it doesn't exist:

        mkdir ~/.virtualenvs
        

    - Create virtualenv (note, I use the word matching below, it can be anything)

        python3 -m venv ~/.virtualenv/matching
        
    - Activate virtualenv 

        source ~/.virtualenv/matching/bin/activate

    - Install requirements::

        pip install -r requirements.txt


B. Edit connections.py 
---------------

    Edit/create the connections.py file. (you might have to create it as it has passwords and is not stored in git)
    - It should look something like:
    
        import MySQLdb
        MYCONNECTION = MySQLdb.connect("localhost", "user", "pass", "db_table")

    
    In an editor, set the username, password, database etc. 
    You can add muliple connections but you'll have to import the correct one into the matchingStuff.py file. 

C. Edit matchingStuff.py 
---------------------------------------------------------------------------
	Edit this file and make sure you have a method for getting your sql query. Look at the getSponsorData method 
	for place to copy and paste. 

D. Edit runme.py 
---------------------------------------------------------------------------
	Edit this file and make sure you have the methods you want to run. 
	You'll need a fetch method at the least. Look at the existing code
	for an example. Then, from the command line:
	
	python runme.py

	

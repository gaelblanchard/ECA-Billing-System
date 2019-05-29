# ECA-Billing-System

Contributor(s): Gael Blanchard(https://github.com/gaelblanchard)

Requirements: Python 3, Tkinter, SQLite3, matplotlib

# Objective(s):
Implement a GUI which uses an underlying SQL database to graph data, search data and create data

### Instructions:

1) Open Terminal Window

2) Go to directory folder with "patient.csv","billing.csv" and "insurance.csv" file

3) Run the program by typing "python3 ECA.py" into the terminal

4) Use program through the gui window that pops up

# Our Data:
3 seperate csv files are provided. Therefore, cleanup is not necessary. However if cleanup was necessary we could incorporate seperate procedures on every csv file following these stipulations:

1. Ensure that there are no duplicate records
2. Ensure that no two patients share
3. Ensure that all billing amounts are numerical and valid

# How it Works:
By first reading our csvs using an sql statement we instantiate our database.We use tkinter to define the gui's options and link functions where necessary to link sql statements to certain options to return graphs or records.

# Going Further:
Testing more datasets with more features we can expand on the amount of functionalities that are available in the program and furthermore expand the amount of visualizations that we provide.

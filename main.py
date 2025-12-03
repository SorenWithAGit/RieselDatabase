from src import createDatabase as cd
from src import tables


"""
To add tables to the database utilize the tables module and class Tables.
The add_Table function accepts three parameters: Table Name, list of Attributes, and
list of Attribute Types.

An example being:
attributes = ["Field", "[Size (acre)]", "[Size (ha)]", "Landuse"]
attribute_types = ["TEXT", "FLOAT", "FLOAT", "INTEGER REFERENCES Landuse (ID)"]
tb = tables.Tables(DB)
tb.add_Table("Fields", attributes, attribute_types)


To clear tables in the database utilize the tables module and class Tables.
The clear_Table function accepts a list of table names to clear.


To delete tables in the database utilize the tables module and class Tables.
the delete_Table function accepts a list of table names to delete.
"""


DB = "Riesel Database.sqlite"
# createDB = cd.createDatabase(DB)

attributes = ["Field", "[Size (acre)]", "[Size (ha)]", "Landuse"]
attribute_types = ["TEXT", "FLOAT", "FLOAT", "INTEGER REFERENCES Landuse (ID)"]
tb = tables.Tables(DB)
tb.add_Table("Fields", attributes, attribute_types)
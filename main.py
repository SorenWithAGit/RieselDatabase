from src import createDatabase as cd
from src import tables


"""
#######################################################################

To add tables to the database utilize the tables module and class 
Tables.
The add_Table function accepts three parameters: Table Name, list of
Attributes, and list of Attribute Types.

An example being:
attributes = ["Field", "[Size (acre)]", "[Size (ha)]", "Landuse"]
attribute_types = ["TEXT", "FLOAT", "FLOAT", "INTEGER REFERENCES 
                    Landuse (ID)"]
tb = tables.Tables(DB)
tb.add_Table("Fields", attributes, attribute_types)

------------------------------------------------------------------------

To clear tables in the database utilize the tables module and class 
Tables.
The clear_Table function accepts a list of table names to clear.

An example being:
tb.clear_Table(["[Field Boundaries]"])

------------------------------------------------------------------------

To delete tables in the database utilize the tables module and class 
Tables. the delete_Table function accepts a list of table names to
delete.

An example being:
tb.delete_Table(["[Field Boundaries]"])

#######################################################################
"""

# Create Database
DB = "Riesel Database.sqlite"
# createDB = cd.createDatabase(DB)

# Connect to Database and add tables
attributes = ["[Field ID]", "Northing", "Easting", "Latitude", "Longitude"]
attribute_types = ["INTEGER REFERENCES Fields (ID)", "Float", "Float", "Float", "Float"]
tb = tables.Tables(DB)
tb.add_Table("[Field Boundaries]", attributes, attribute_types)

# Clear Tables if Necessary
# tb.clear_Table(["[Field Boundaries]"])

# Delete Tables if Necessary
# tb.delete_Table(["[Field Boundaries]"])
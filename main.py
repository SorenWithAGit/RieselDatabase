import sqlite3
import pandas as pd
from src import createDatabase as cd
from src import tables
from src import dates

DB = "Riesel Database.sqlite"

"""
CREATE DATABASE
#######################################################################

To create an SQLITE database utilize the module createDB and class
createDatabase which accepts one paramater a string of the filename.

An example being
DB = "Riesel Database.sqlite"
# createDB = cd.createDatabase(DB)

#######################################################################
"""
# Create Database
# createDB = cd.createDatabase(DB)


"""
ADD TABLES
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

#######################################################################
"""

# attributes = ["[Rain Gauge ID]", "[Date ID]",
#               "[Measured Precip (mm)]"]
# attribute_types = ["INTEGER REFERENCES [Rain Gauges] (ID)", 
#                    "INTEGER REFERENCES Dates (ID)",
#                    "FLOAT"]
# tb = tables.Tables(DB)
# tb.add_Table("[Precipitation]", attributes, attribute_types)


"""
ADD COLUMNS
#######################################################################

To add a column to a table utilize the tables module and class
Tables and function add_attributes which accepts three parameters: 
a string of the table name, a list of table attributes, and a list of
table attribute types.

An example being:
tb = tables.Tables(DB)
tb.add_attributes("Seasons", ["[Start Date]", "[End Date]"], ["TEXT", "TEXT"])

#######################################################################
"""

# tb = tables.Tables(DB)
# tb.add_attributes("Seasons", ["[Start Date]", "[End Date]"], ["TEXT", "TEXT"])


"""
REMOVE COLUMNS
#######################################################################

To remove a column from a table utilize the tables module and class
Tables and function remove_column which accepts two parameters:
a string of the table name, and a list of attributes to remove.

An example being:
tb = tables.Tables(DB)
tb.remove_column("Seasons", ["[Start Date]", "[End Date]"])

#######################################################################
"""


"""
RENAME COLUMNS
#######################################################################

To rename an attribute in a table utilize the tables module and class
Tables and function rename_columns which accepts three parameters:
a string of the table name, a list of old attribute names, and a
list of new attribute names

An example being:
tb = tables.Tables(DB)
tb.rename_columns("Seasons", ["[Start Date]", "[End Date]"], 
                    ["Begins", "Ends"])

#######################################################################
"""


"""
REMOVE SPECIFIED ENTRIES
#######################################################################

To remove entries from a table utilize the tables module and class
Tables and function remove_entry which accepts two parameters:
a string of the table name, and a list of ids corresponding to the id
attribute in the table:

An example being:
tb = tables.Tables(DB)
tb.remove_entry("Year", [12, 15, 17])

#######################################################################
"""

# tb = tables.Tables(DB)
# tb.remove_entry("Year", [12, 15, 17])


"""
CLEAR TABLE
#######################################################################

To clear tables in the database utilize the tables module and class 
Tables.
The clear_Table function accepts a list of table names to clear.

An example being:
tb = tables.Tables(DB)
tb.clear_Table(["[Field Boundaries]"])

#######################################################################
"""

# tb = tables.Tables(DB)
# tb.clear_Table(["[Field Boundaries]"])


"""
DELETE TABLE
#######################################################################

To delete tables in the database utilize the tables module and class 
Tables. the delete_Table function accepts a list of table names to
delete.

An example being:
tb = tables.Tables(DB)
tb.delete_Table(["[Field Boundaries]"])

#######################################################################
"""

# tb = tables.Tables(DB)
# tb.delete_Table(["[Field Boundaries]"])


"""
DATE DATAFRAME
#######################################################################

To create a panadas DataFrame containing all dates within a date range
utilize the module dates, class date_range, and function generate_dates
which accepts two parameters a start date, and end date. Witht the 
format: YYYY,MM,DD.

An example being:
date_df = dates.date_range.generate_dates("1937-01-01", "2025-12-31")

#######################################################################
"""

# Create pandas DataFrame with provided dates
# date_df = dates.date_range.generate_dates("1937-01-01", "2025-12-31")


"""
ADD DATES
#######################################################################

To add dates to the database from the returned DataFrame utilize the
module dates, class db_dates, and function add_dates which accepts a 
datafrmae as the only parameter (generated above).

An example being:
Dates = dates.db_dates(DB)
Dates.add_dates(date_df)

#######################################################################
"""

# Connect to Database and add dates from DataFrame
# Dates = dates.db_dates(DB)
# Dates.add_dates(date_df)


"""
YEAR DATAFRAME
#######################################################################

To create a panadas DataFrame containing all years within a date range
utilize the module dates, class date_range, and function generate_years
which accepts two parameters a start date, and end date. Witht the 
format: YYYY,MM,DD.

An example being:
year_df = dates.date_range.generate_years("1937-01-01", "2025-12-31")

#######################################################################
"""

# year_df = dates.date_range.generate_years("1937-01-01", "2025-12-31")


"""
ADD YEAR
#######################################################################

To add years to the database from the returned DataFrame utilize the
module dates, class db_dates, and function add_years which accepts a 
datafrmae as the only parameter (generated above).

An example being:
years = dates.db_dates(DB)
years.add_years(year_df)

#######################################################################
"""

# years = dates.db_dates(DB)
# years.add_years(year_df)


"""
ADD SEASONS
#######################################################################

To add seasons to the database utilize the module dates, class seasons,
and function add_seasons.

An example being:
seasons = dates.seasons(DB)
seasons.add_seasons()

#######################################################################
"""

# seasons = dates.seasons(DB)
# seasons.add_seasons()

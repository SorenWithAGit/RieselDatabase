from src import createDatabase as cd
from src import tables
from src import dates

DB = "Riesel Database.sqlite"

"""
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
tb = tables.Tables(DB)
tb.clear_Table(["[Field Boundaries]"])

------------------------------------------------------------------------

To delete tables in the database utilize the tables module and class 
Tables. the delete_Table function accepts a list of table names to
delete.

An example being:
tb = tables.Tables(DB)
tb.delete_Table(["[Field Boundaries]"])

#######################################################################
"""

# Connect to Database and add tables
# attributes = ["[Field ID]", "Northing", "Easting", "Latitude", "Longitude"]
# attribute_types = ["INTEGER REFERENCES Fields (ID)", "Float", "Float", "Float", "Float"]
# tb = tables.Tables(DB)
# tb.add_Table("[Field Boundaries]", attributes, attribute_types)

# Clear Tables if Necessary
# tb.clear_Table(["[Dates]"])

# Delete Tables if Necessary
# tb.delete_Table(["[Field Boundaries]"])


"""
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
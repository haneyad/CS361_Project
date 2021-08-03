# import Craigslist job search module
from craigslist import CraigslistJobs
import mariadb
import sys

# List of craigslist sites to interrogate
cl_sites = ['annarbor', 'centralmich', 'battlecreek', 'detroit', 'grandrapids', 'flint', 'holland', 'jackson',
            'kalamazoo', 'lansing', 'monroe', 'muskegon', 'nmi', 'porthuron', 'swmi', 'thumb', 'up',
            'columbiamo', 'joplin', 'kansascity', 'kirksville', 'loz', 'semo', 'springfield', 'stjoseph',
            'stlouis', 'fayar', 'fortsmith', 'jonesboro', 'littlerock', 'texarkana', 'chattanooga',
            'clarksville', 'cookeville', 'jacksontn', 'knoxville', 'memphis', 'nashville', 'tricities',
            'ames', 'cedarrapids', 'desmoines', 'dubuque', 'fortdodge', 'iowacity', 'masoncity',
            'quadcities', 'siouxcity', 'ottumwa', 'waterloo', 'bn', 'chambana', 'chicago', 'decatur',
            'lasalle', 'mattoon', 'peoria', 'rockford', 'carbondale', 'springfieldil', 'quincy',
            'lawton', 'enid', 'oklahomacity', 'stillwater', 'tulsa',
            ]

# List of craigslist categories to interrogate; engineering, manufacturing, software dev, etc.
cl_categories = ['egr', 'mnu', 'sof', 'sad', 'sci', 'web', 'mnu']

site_index = 0
cat_index = 0

# result list from query; each item in the list is a dictionary. Items will be split into columns and pushed
# to MariaDB
""" 
Keys for dictionary:
id = value is string
name = value is string
url = value is string
last_update = value is string
where = value is string

other keys in each item but not desired to push
"""
result_list = [];

# Run a query of sites/categories and push into result_list
for site_index in range(0, len(cl_sites)):
    for cat_index in range(0, len(cl_categories)):
        cl_j = CraigslistJobs(site=str(cl_sites[site_index]), category=str(cl_categories[cat_index]),
                              filters={'employment_type': ['full-time']})
        for result in cl_j.get_results():
            result_list.append(result)

# get key list from result dictionary returned by craiglist module
keyz = result_list[0].keys()

for results in result_list:
    print(results)

# Connect with MariaDB on OSU servers
try:
    conn = mariadb.connect(
        user='cs361_haneyad',
        password='PussyEater898!',
        host='classmysql.engr.oregonstate.edu',
        database='cs361_haneyad')
except mariadb.Error as e:
    print(f"Error connecting to Maria DB: {e}")
    sys.exit(1)

# get cursor
cur = conn.cursor()

# DELETE all rows from table
#cur.execute("DELETE FROM cl_jobsdata")

try:
    # split data from result_list and insert to MariaDB
    for result in result_list:
        id_val = result['id']
        name_val = result['name']
        url_val = result['url']
        last_updated_val = result['last_updated']
        where_val = result['where']
        cur.execute("INSERT INTO cl_jobsdata (id, last_update, location, name, url) VALUES (?, ?, ?, ?, ?)",
                    (str(id_val), str(last_updated_val), str(where_val), str(name_val), str(url_val)))
except mariadb.Error as e:
    print(f"Error: {e}")

conn.commit()
print(f"Last Inserted ID: {cur.lastrowid}")
conn.close()

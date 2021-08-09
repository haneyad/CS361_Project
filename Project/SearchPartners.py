# import Craigslist job search module
from craigslist import CraigslistJobs, CraigslistServices, CraigslistForSale, CraigslistCommunity

import mariadb
import sys


def db_conn_write(dbName, dataList, deleteAll):
    try:
        conn = mariadb.connect(
            user='cs361_haneyad',
            password='PussyEater898!',
            host='classmysql.engr.oregonstate.edu',
            database='cs361_haneyad')
    except mariadb.Error as error:
        print(f"Error connecting to Maria DB: {error}")
        sys.exit(1)

    # get cursor
    cur = conn.cursor()

    # DELETE all rows from table
    if deleteAll:
        cur.execute("DELETE FROM " + dbName)

    try:
        # split data from result_list and insert to MariaDB
        for result in dataList:
            id_val = result['id']
            name_val = result['name']
            url_val = result['url']
            last_updated_val = result['last_updated']
            where_val = result['where']
            cur.execute("INSERT INTO " + dbName + " (id, last_update, location, name, url) VALUES (?, ?, ?, ?, ?)",
                        (str(id_val), str(last_updated_val), str(where_val), str(name_val), str(url_val)))
    except mariadb.Error as error:
        print(f"Error: {error}")

    conn.commit()
    print(f"Last Inserted ID: {cur.lastrowid}")
    conn.close()


def wine_search(argCityList):
    wine_list = []

    # Run a query of sites/categories and push into result_list
    for index in range(0, len(argCityList)):
        cl_sale = CraigslistForSale(site=str(cl_sites[index]),
                                    filters={'query': 'wine', 'has_image': 'True', 'search_titles': 'True',
                                             'bundle_duplicates': 'True'})
        for hit in cl_sale.get_results():
            wine_list.append(hit)
            print(hit)

    return wine_list


def personal_search(argCityList):
    personal_list = []

    # Run a query of sites/categories and push into result_list
    for index in range(0, len(argCityList)):
        cl_sale = CraigslistForSale(site=str(cl_sites[index]), category='mis',
                                    filters={'search_titles': 'True', 'bundle_duplicates': 'True'})
        for hit in cl_sale.get_results():
            personal_list.append(hit)
            print(hit)

    return personal_list


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

import requests
import hashlib
import csv
import sqlite3
import datetime
import time
import io

DATABASE = 'data.db'
LINKLIST = 'link_list.csv'


def get_url_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        url_list = csv.reader(file, delimiter=',')
        return [row for row in url_list]


def get_url_content(url):
    return requests.get(url,).text.replace("'", "''") # удваиваю одинарную кавычку, что бы можно было вставить в БД


def apply_sql_query(query):
    connection = sqlite3.connect(DATABASE).cursor().executescript(query)
    connection.close()


def create_db():
    db_create_query = '''CREATE TABLE url(url text, content text, date text)'''
    apply_sql_query(db_create_query)


def add_content_to_db(url_list):
    for url in url_list:
        url_content = get_url_content(url[0])
        time.sleep(1)
        content_inser_query = '''insert into content_tab(url, content, date) VALUES('{0}', '{1}', '{2}')'''.format(
            str(url[0]), url_content, str(int(datetime.datetime.now().timestamp())))
        apply_sql_query(content_inser_query)


add_content_to_db(get_url_list(LINKLIST))

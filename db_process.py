import sqlite3
import os.path

# conn_snorkel = sqlite3.connect('snorkel.db')


def create_tables(name):
    """
    Creates a tables
    :param name: Name of the new DB
    :return: None
    """
    if os.path.isfile(name+'.db'):
        os.remove(name+'.db')
    conn_new = sqlite3.connect(name+'.db')
    c = conn_new.cursor()
    c.execute('CREATE TABLE document ('
              'id INTEGER PRIMARY KEY AUTOINCREMENT,'
              'text TEXT NOT NULL,'
              'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,'
              'version INTEGER)')

    c.execute('CREATE TABLE sentence ('
              'id INTEGER PRIMARY KEY AUTOINCREMENT,'
              'text TEXT NOT NULL,'
              'doc_id INTEGER, '
              'position INTEGER,'
              'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,'
              'version INTEGER,'
              'FOREIGN KEY(doc_id) REFERENCES document(id))')

    conn_new.commit()
    c.close()


create_tables('test')


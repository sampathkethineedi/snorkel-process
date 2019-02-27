import sqlite3
import os.path


class DataBase(object):
    def __init__(self, name):
        """
        Create DB connection
        :param name: Database name
        """
        self.name = name
        if os.path.isfile(self.name + '.db'):
            os.remove(self.name + '.db')
        self.conn = sqlite3.connect(self.name + '.db')

    def create_tables(self):
        """
        Creates tables
        :return: None
        """
        c = self.conn.cursor()
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

        self.conn.commit()
        c.close()

    def push_sentence_table(self, sentence_data):
        """
        Insert Snorkel sentence data into DB
        :param sentence_data: Snorkel sentence data
        :return: None
        """
        c = self.conn.cursor()
        for item in sentence_data:
            c.execute('insert into sentence(doc_id,position,text,version) values (?,?,?,?)', (*item, 1))
        self.conn.commit()
        c.close()


def get_snorkelDB_data():
    """
    Get data from snorkel
    :return: sentence_data
    """
    conn_snorkel = sqlite3.connect('snorkel.db')
    c = conn_snorkel.cursor()
    c.execute('SELECT document_id,position,text FROM sentence')
    sentence_data = c.fetchall()
    c.close()
    return sentence_data


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run DB process')
    parser.add_argument('-n', '--name', dest='name', required=True, help='DB name')
    args = parser.parse_args()

    test_db = DataBase(args.name)
    test_db.create_tables()
    sent_data = get_snorkelDB_data()
    test_db.push_sentence_table(sent_data)
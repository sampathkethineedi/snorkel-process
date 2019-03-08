import sqlite3
import os.path
from snorkel import SnorkelSession


class DataBase(object):
    def __init__(self, name, version=0.1):
        """
        Create DB connection
        :param name: Database name
        """
        self.session = SnorkelSession()
        self.name = name
        self.version = version
        if os.path.isfile('DB/'+self.name + '_output.db'):
            os.remove('DB/'+self.name + '_output.db')
        self.conn = sqlite3.connect('DB/'+self.name + '_output.db')

    def create_tables(self):
        """
        Creates tables
        :return: None
        """
        c = self.conn.cursor()

        c.execute('CREATE TABLE document ('
                  'id INTEGER PRIMARY KEY,'
                  'text TEXT NOT NULL,'
                  'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,'
                  'version INTEGER)')

        c.execute('CREATE TABLE sentence ('
                  'id INTEGER PRIMARY KEY,'
                  'text TEXT NOT NULL,'
                  'document_id INTEGER, '
                  'position INTEGER,'
                  'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,'
                  'version INTEGER,'
                  'FOREIGN KEY(document_id) REFERENCES document(id))')

        c.execute('CREATE TABLE label ('
                  'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                  'sentence_id INTEGER,'
                  'document_id INTEGER,'
                  'probability FLOAT,'
                  'lf_func INTEGER,'
                  'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,'
                  'FOREIGN KEY(sentence_id) REFERENCES sentence(id),'
                  'FOREIGN KEY(document_id) REFERENCES sentence(document_id))')

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
            c.execute('insert into sentence(id, document_id,position,text,version) '
                      'values (?,?,?,?,?)', (*item, self.version))
        self.conn.commit()
        c.close()

    def push_label_table(self, label_data):
        """
        Insert Snorkel sentence data into DB
        :param label_data: Snorkel label data
        :return: None
        """
        c = self.conn.cursor()
        for item in label_data:
            c.execute('insert into label(document_id,sentence_id,lf_func,probability) '
                      'values (?,?,?,?)', item)
        self.conn.commit()
        c.close()


def get_sentence_data(name):
    """
    Obtain sentence data from DB
    :return: sentence_data
    """
    conn_snorkel = sqlite3.connect('DB/'+name+'_snorkel.db')
    c = conn_snorkel.cursor()
    c.execute('SELECT id, document_id,position,text '
              'FROM sentence')
    sentence_data = c.fetchall()
    c.close()
    return sentence_data


def get_label_data(name):
    """
    Perform product and obtain mariginals data
    :return: label_data
    """
    conn_snorkel = sqlite3.connect('DB/'+name+'_snorkel.db')
    c = conn_snorkel.cursor()
    c.execute('SELECT document_id,sentence.id,value,probability '
              'FROM text,sentence,marginal,span '
              'WHERE candidate_id = text.id '
              'AND text.text_id = span.id '
              'AND span.sentence_id = sentence.id')
    label_data = c.fetchall()
    c.close()
    return label_data


def db_process(name):
    """
    Main DB process
    :param name: name of the DB
    :return:
    """
    test_db = DataBase(name)
    test_db.create_tables()
    sent_data = get_sentence_data(name)
    lab_data = get_label_data(name)
    test_db.push_sentence_table(sent_data)
    test_db.push_label_table(lab_data)

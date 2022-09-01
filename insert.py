import json
from datetime import datetime
from elasticsearch import Elasticsearch
from time import sleep

es = Elasticsearch('http://192.168.14.254:9200')


def start_insert():
    while True:
        insert_to_es()
        sleep_time = 5*60
        sleep(sleep_time)


def insert_to_es():

    current_date = datetime.now()

    f = open('./data/shifts.json', 'r')
    data = json.loads(f.read())

    if data != []:
        for row in data:
            dateDebut = datetime.strptime(row['dateDebut'], '%Y-%m-%d %H:%M:%S.%f')
            dateFin = datetime.strptime(row['dateFin'], '%Y-%m-%d %H:%M:%S.%f')

            if dateDebut < current_date < dateFin:
                doc = {
                    'shiftId': row['idShift'],
                    'codeArticle': row['codeArticle'],
                    'poids': row['poids'],
                    'timestamp': datetime.now()
                }
                es.index(index="acome", document=doc)

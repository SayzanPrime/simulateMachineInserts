from utils import getPlaningMachine, getShitfsByPlaningId, getArticleByMachineId

from datetime import datetime, date

from config import settings

import psycopg2
import psycopg2.extras

import json
from time import sleep


def start_traitement():
    while True:
        traitement()
        sleep_time = 30*60
        sleep(sleep_time)


def traitement():
    current_date = datetime.now()

    # Connect to postgresql
    cnx = psycopg2.connect(
        host=settings.PG_HOST,
        port=settings.PG_PORT,
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        database=settings.PG_DATABASE_NAME
    )

    cursor = cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Get planing maching
    planings = getPlaningMachine(cursor)

    # Get shifts from each planing
    toInsert = []

    for planing in planings:
        # Check if the current date is within the date range of the planing
        if planing['date_debut'] <= date.today() <= planing['date_fin']:

            # Get shifts that within the planing
            shifts = getShitfsByPlaningId(cursor, planing['id_planing'])
            article = getArticleByMachineId(cursor, planing['id_machine'])

            for shift in shifts:
                date_debut = current_date.replace(
                    hour=int(shift['heure_debut'].split(':')[0]), minute=int(shift['heure_debut'].split(':')[1]))

                date_fin = current_date.replace(
                    hour=int(shift['heure_fin'].split(':')[0]), minute=int(shift['heure_fin'].split(':')[1]))

                doc = {
                    'idShift': shift['id_shift'],
                    'dateDebut': date_debut,
                    'dateFin': date_fin,
                    'codeArticle': article['code_article'],
                    'poids': article['poids'],
                    'objectif_kg': article['objectif_kg'],
                }

                toInsert.append(doc)

            break

    with open('./data/shifts.json', 'w', encoding='UTF8') as d:
        json.dump(toInsert, d, indent=4, default=str)

    cursor.close()
    cnx.close()

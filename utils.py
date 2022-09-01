def getPlaningMachine(cursor):
    try:
        cursor.execute(
            "select * from planing_machine where id_planing is not null"
        )
        return cursor.fetchall()
    except Exception as e:
        print('Error -> ', e)


def getShitfsByPlaningId(cursor, idPlaning: int):
    try:
        cursor.execute(
            "select * from shift where id_planing is not null and id_planing = %s",
            [idPlaning]
        )
        return cursor.fetchall()
    except Exception as e:
        print('Error -> ', e)


def getArticleByMachineId(cursor, idMachine: int):
    try:
        cursor.execute(
            "select * from type_article where id_machine = %s", [idMachine]
        )
        return cursor.fetchone()
    except Exception as e:
        print('Error -> ', e)

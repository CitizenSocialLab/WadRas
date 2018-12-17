__author__ = 'julian'

import csv
import MySQLdb
import datetime
import game.vars as VARS

def get_data_sql():

    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='',
                         db='wadras',
                         charset='utf8',
                         use_unicode=False)
    cursor = db.cursor()

    participants = "SELECT R.original_id, R.selection, P.seleccio1 FROM game_prisoner P " \
                   "LEFT JOIN game_resident R ON P.rival1_resident_id = R.id "


    actions_participants = []
    cursor.execute(participants)
    results = cursor.fetchall()
    for row in results:
        actions_participants.append([row[0], row[1], row[2]])
    db.close()

    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='',
                         db='wadras_session',
                         charset='utf8',
                         use_unicode=False)
    cursor = db.cursor()

    users = "SELECT U.id, U.nickname, U.money_game1, U.money_game2, U.money_game3, U.money_game4 " \
            "FROM game_user U WHERE is_robot=0"
    actions_residents = []
    cursor.execute(users)
    results = cursor.fetchall()
    for row in results:
        actions_residents.append([row[0], row[1], row[2], row[3], row[4], row[5]])
    db.close()


    for u in actions_residents:
        selections_participants = [a[2] for a in actions_participants if a[0] == u[0]]
        d = {x:selections_participants.count(x) for x in selections_participants}

        ## Individual actions
        a, b = d.keys(), d.values()
        C, D = 0, 0
        for index, action in enumerate(a):
            if action == 'C':
                C = b[index]
            if action == 'D':
                D = b[index]

        ## Global action
        if C >= D: action_participants = 'C'
        else: action_participants = 'D'

        ## Selection resident
        selection_resident = [a[1] for a in actions_participants if a[0] == u[0]][0]

        ## Results
        if selection_resident == "C":
            if action_participants == "C":
                result = VARS.MATRIX1[0][0]
            elif action_participants == "D":
                result = VARS.MATRIX1[1][0]
            else:
                result = 0

        elif selection_resident == "D":
            if action_participants == "C":
                result = VARS.MATRIX1[2][0]
            elif action_participants == "D":
                result = VARS.MATRIX1[3][0]
            else:
                result = 0

        print '%s (%d) - Games: %d + %d + %d = %d Action = [%s, %s]' %(u[1], u[0], u[2], u[3], result, u[2]+u[3]+result, selection_resident, action_participants)

    return None

get_data_sql()
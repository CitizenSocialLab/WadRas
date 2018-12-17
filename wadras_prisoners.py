__author__ = 'julian'

import csv
import MySQLdb
import datetime

def get_data_sql():

    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='',
                         db=name_db,        # Name Database
                         charset='utf8',
                         use_unicode=False)
    cursor = db.cursor()

    #Todo: Fer aquesta crida amb una sentence
    participants = "SELECT U.id, U.nickname, P.seleccio1, P.partida_id FROM game_user U " \
                   "LEFT JOIN game_prisoner P ON P.user_id= U.id " \
                   "WHERE U.is_robot = 0"

    games = "SELECT G.id FROM game_partida G " \
                   "WHERE G.classe = 'voice'"


    valid_games = []
    cursor.execute(games)
    results = cursor.fetchall()
    for row in results:
        valid_games.append(row[0])

    users = []
    cursor.execute(participants)
    results = cursor.fetchall()
    for row in results:
        for g in valid_games:
            if row[3] == g:
                user = {'id': row[0],
                        'nickname' : row[1],
                        'selection' : row[2]}
                users.append(user)

    print "-------"
    print " Load  "
    print "-------"

    db.close()

    return users


def get_data_xls():

    users = []

    file = open('residents.csv','rU')

    csv_data = csv.reader(file)
    header = csv_data.next()

    for row in csv_data:
        user = {'id': row[0],
                'nickname' : row[1],
                'name': row[2],
                'selection' : row[3]}
        users.append(user)

    return users

def save_data(users):

    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='',
                         db=name_db,        # Name Database
                         charset='utf8',
                         use_unicode=False)
    cursor = db.cursor()

    for u in users:
        try:
            print u['name']
            cursor.execute("INSERT INTO game_resident(original_id, nickname, name, selection, last_selected) "
                       "VALUES(%s, %s, %s, %s, %s)",[u['id'], u['nickname'], u['name'], u['selection'], datetime.datetime.utcnow()])
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    db.commit()
    cursor.close()
    print "-------"
    print " Saved "
    print "-------"


users = get_data_xls()
save_data(users)

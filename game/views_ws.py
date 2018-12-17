from django.views.decorators.csrf import csrf_exempt

from game.models import *
from game.vars import *
import math

from django.shortcuts import redirect


import datetime
from django.utils import timezone

import json
from django.http import HttpResponse


import random
random.seed(datetime.datetime.now())

@csrf_exempt
def enviar_joc(request, **kwargs):
    #ToDo: Changes the names from CA to EN
    id_joc = kwargs.get('id_joc', None)

    if(id_joc == "01"): game_name = "standard"
    if(id_joc == "02"): game_name = "interact"
    if(id_joc == "03"): game_name = "voice"
    if(id_joc == "04"): game_name = "wall"

    print 'Game: '+ game_name

    response_data={}
    # Save in the the session the game variable
    request.session['game'] = game_name
    # Save in the database the game variable
    game = Game()
    game.name = game_name

    game.save()

    response_data['joc_saved'] = "Ok"

    return HttpResponse(json.dumps(response_data),content_type="application/json")


@csrf_exempt
def demanar_dades(request, **kwargs):
    #ToDo L'usuari que espera esta aqui demanant dades
    user_id = kwargs.get('user_id', None)

    response_data={}
    jugant = "false"

    user = None
    try:
        # partida que juga aquest usuari
        user = User.objects.get(id=user_id)
    except:
        print "Usuari "+str(user_id)+" no existeix"

    if user.partida_current is None:
        response_data["jugant"] = "false"
        response_data["error"] = "GAME DOES NOT EXIST"
        return HttpResponse(json.dumps(response_data),content_type="application/json")


    #ToDO: Aixo ho tenim que fer per cada un del tipos de partides
    if user.partida_current.estat == "JUGANT":
        jugant = "true"

    response_data["jugant"] = jugant
    return HttpResponse(json.dumps(response_data),content_type="application/json")


###############################################################################################
#################################### PRISONER 1 ###############################################
###############################################################################################

@csrf_exempt
def enviar_accio_prisoner1(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

        if result=='C' or result=='D':
            if user_prisoner.seleccio1 == "":
                user_prisoner.seleccio1 = result
                user_prisoner.is_robot1 = False
                user_prisoner.data_seleccio1 = timezone.localtime(timezone.now())

                user_prisoner.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def enviar_accio_guess1(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

        if result=='C' or result=='D':
            if user_prisoner.guess1 == "":
                user_prisoner.guess1 = result
                user_prisoner.data_guess1 = timezone.localtime(timezone.now())
                user_prisoner.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def demanar_resultat_prisoner1(request, **kwargs):

    user_id = kwargs.get('user_id', None)
    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"correcte": False,
                         "error": "GAME DOES NOT EXIST"}
    else:

        # Data user and selection
        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)
        selection = user_prisoner.seleccio1

        # Standard and Interact
        # Get data rival
        if user.partida_current.classe == 'standard' or user.partida_current.classe == 'interact':
            user_prisoner_rival = Prisoner.objects.get(user=user_prisoner.rival1.id, partida=user.partida_current)
            selection_rival = user_prisoner_rival.seleccio1

            if selection_rival == "":
                # The rival do not answer yet.
                response_data = {"correcte": False}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                if user_prisoner_rival.is_robot1:
                    print 'Rival robot'

        # Voice
        # No rival selection
        if user.partida_current.classe == 'voice':
            selection_rival = ""

        # Wall
        # Get rival selection
        if user.partida_current.classe == 'wall':
            selection_rival = user_prisoner.rival1_resident.selection

        # Calculate results
        if selection == "C":
            print 'selection C'
            if selection_rival == "C":
                resultat_prisoner1 = MATRIX1[0][0]
            elif selection_rival == "D":
                resultat_prisoner1 = MATRIX1[1][0]
            else:
                resultat_prisoner1 = 0

        elif selection == "D":
            print 'selection C'
            if selection_rival == "C":
                resultat_prisoner1 = MATRIX1[2][0]
            elif selection_rival == "D":
                resultat_prisoner1 = MATRIX1[3][0]
            else:
                resultat_prisoner1 = 0


        print '-------------------'
        print user.partida_current.classe
        print selection_rival
        print resultat_prisoner1
        print '-------------------'

        user_prisoner.gain1 = resultat_prisoner1
        user_prisoner.save()

        if user_prisoner.partida.classe == 'standard': user.money_game1 = user_prisoner.gain1
        if user_prisoner.partida.classe == 'interact': user.money_game2 = user_prisoner.gain1
        if user_prisoner.partida.classe == 'voice': user.money_game3 = user_prisoner.gain1
        if user_prisoner.partida.classe == 'wall': user.money_game4 = user_prisoner.gain1

        user.punts_totals = (user.money_game1) + \
                            (user.money_game2) + \
                            (user.money_game3) + \
                            (user.money_game4)

        user.save()

        response_data = {"correcte": True,
                         "game": request.session['game'],
                         "seleccio": selection,
                         "oponent": selection_rival,
                         "max_points": TOTAL_MAX1}

        return HttpResponse(json.dumps(response_data), content_type="application/json")


###############################################################################################
################         WEBSERVICES RESULTATS FINAL JOC      #################################
###############################################################################################

@csrf_exempt
def demanar_resultat_partida(request, **kwargs):
    print 'Demanar resultat Public Game'

@csrf_exempt
def tancar_partida(request, **kwargs):

    response_data = {}
    id = kwargs.get('num_partida', None)
    partida = Partida.objects.get(id=id)

    partida.estat = 'ACABADA_MANUAL'
    partida.data_finalitzacio = timezone.localtime(timezone.now())

    partida.save()

    users = User.objects.filter(partida_current=partida)

    for u in users:
        print u.id
        u.partida_current = None
        print u.partida_current
        u.save()

    response_data["correcte"] = False
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def llistat_partides(request, **kwargs):

    response_data = {}

    all_partides = []
    for partida in Partida.objects.order_by('-id'):

        if partida.classe == "standard":
            partida.classe ="Standard"
            users = [u.id for u in User.objects.filter(game1=partida.id)]

        elif partida.classe == "interact":
            partida.classe ="Interact"
            users = [u.id for u in User.objects.filter(game2=partida.id)]

        elif partida.classe == "voice":
            partida.classe ="Voice"
            users = [u.id for u in User.objects.filter(game3=partida.id)]

        elif partida.classe == "wall":
            partida.classe ="Wall"
            users = [u.id for u in User.objects.filter(game4=partida.id)]


        data_partida = {"id": partida.num_partida,
                        "data_creacio": partida.data_creacio.strftime("%a, %H:%M:%S") if partida.data_creacio else '-',
                        "data_inicialitzacion": partida.data_inicialitzacio.strftime("%a, %H:%M:%S") if partida.data_inicialitzacio else '-',
                        "data_finalitzacio": partida.data_finalitzacio.strftime("%a, %H:%M:%S") if partida.data_finalitzacio else '-',
                        "estat": partida.estat,
                        "classe": partida.classe,
                        "players": users,
        }
        all_partides.append(data_partida)
    response_data["partida"] = all_partides

    return HttpResponse(json.dumps(response_data), content_type="application/json")


###############################################################################################
###############################         PARTIDES      #########################################
###############################################################################################

@csrf_exempt
def estat_partida(request, **kwargs):
    response_data = {}

    game1 = Partida.objects.filter(classe="standard")
    game2 = Partida.objects.filter(classe="interact")
    game3 = Partida.objects.filter(classe="voice")
    game4 = Partida.objects.filter(classe="wall")

    ##########
    # Darrera partida acabada
    ##########
    last_finished_game1 = Partida.objects.filter(classe="standard").filter(estat="ACABADA").order_by("data_finalitzacio").last()
    if last_finished_game1 is None:
        response_data['last_finished_game1'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(game1=last_finished_game1.id)]
        partida = {'id': last_finished_game1.id,
                   'classe': last_finished_game1.classe,
                   'estat': last_finished_game1.estat,
                   'dia': (last_finished_game1.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if last_finished_game1.data_creacio else '-',
                   'usuaris_registrats': last_finished_game1.usuaris_registrats,
                   "data_finalitzacio": (last_finished_game1.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['last_finished_game1'] = partida

    last_finished_game2 = Partida.objects.filter(classe="interact").filter(estat="ACABADA").order_by("data_finalitzacio").last()
    if last_finished_game2 is None:
        response_data['last_finished_game2'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(game2=last_finished_game2.id)]
        partida = {'id': last_finished_game2.id,
                   'classe': last_finished_game2.classe,
                   'estat': last_finished_game2.estat,
                   'dia': (last_finished_game2.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if last_finished_game2.data_creacio else '-',
                   'usuaris_registrats': last_finished_game2.usuaris_registrats,
                   "data_finalitzacio": (last_finished_game2.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['last_finished_game2'] = partida

    last_finished_game3 = Partida.objects.filter(classe="voice").filter(estat="ACABADA").order_by("data_finalitzacio").last()
    if last_finished_game3 is None:
        response_data['last_finished_game3'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(game3=last_finished_game3.id)]
        partida = {'id': last_finished_game3.id,
                   'classe': last_finished_game3.classe,
                   'estat': last_finished_game3.estat,
                   'dia': (last_finished_game3.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if last_finished_game3.data_creacio else '-',
                   'usuaris_registrats': last_finished_game3.usuaris_registrats,
                   "data_finalitzacio": (last_finished_game3.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['last_finished_game3'] = partida


    last_finished_game4 = Partida.objects.filter(classe="wall").filter(estat="ACABADA").order_by("data_finalitzacio").last()

    if last_finished_game4 is None:
        response_data['last_finished_game4'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(game4=last_finished_game4.id)]

        partida = {'id': last_finished_game4.id,
                   'classe': last_finished_game4.classe,
                   'estat': last_finished_game4.estat,
                   'dia': (last_finished_game4.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if last_finished_game4.data_creacio else '-',
                   'usuaris_registrats': last_finished_game4.usuaris_registrats,
                   "data_finalitzacio": (last_finished_game4.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['last_finished_game4'] = partida

    #######
    ## Partides actives
    #######

    partides = []
    for p in game1:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['actives_game1'] = partides

    partides = []
    for p in game2:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['actives_game2'] = partides

    partides = []
    for p in game3:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['actives_game3'] = partides

    partides = []
    for p in game4:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['actives_game4'] = partides



    return HttpResponse(json.dumps(response_data), content_type="application/json")

###############################################################################################
##################################         USERS      #########################################
###############################################################################################

@csrf_exempt
def estat_users(request, **kwargs):
    response_data = {}

    users_con_partida_activa = User.objects.filter(~models.Q(partida_current = None) & ~models.Q(is_robot = 1)).order_by('partida_current')
    users = []
    for u in users_con_partida_activa:

        jugades = []
        no_jugades = []

        if u.date_end_game1:
            jugades.append(' Game 1')
        else:
            no_jugades.append(' Game 1')

        if u.date_end_game2:
            jugades.append(' Game 2')
        else:
            no_jugades.append(' Game 2')

        if u.date_end_game3:
            jugades.append(' Game 3')
        else:
            no_jugades.append(' Game 3')

        if u.date_end_game4:
            jugades.append(' Game 4')
        else:
            no_jugades.append(' Game 4')

        if u.session_game == "standard": u.session_game="Standard"
        elif u.session_game == "interact": u.session_game="Interact"
        elif u.session_game == "voice": u.session_game="Voice"
        elif u.session_game == "wall": u.session_game="Wall"

        if u.partida_current.classe == "standard": u.partida_current.classe ="Standard"
        elif u.partida_current.classe == "interact": u.partida_current.classe ="Interact"
        elif u.partida_current.classe == "voice": u.partida_current.classe ="Voice"
        elif u.partida_current.classe == "wall": u.partida_current.classe ="Wall"

        user = {'id': u.id,
                'estat_user': u.status,
                'session_game': u.session_game,
                'partida': u.partida_current.id,
                'classe': u.partida_current.classe,
                'estat': u.partida_current.estat,
                'jugades': jugades,
                'no_jugades': no_jugades}
        users.append(user)
    response_data['users'] = users


    users_all = User.objects.filter(is_robot = 0).order_by('-updated_at')
    users_all_array = []

    for u in users_all:

        if u.session_game == "standard": u.session_game="Standard"
        elif u.session_game == "interact": u.session_game="Interact"
        elif u.session_game == "voice": u.session_game="Voice"
        elif u.session_game == "wall": u.session_game="Wall"


        # Partida activa
        if u.partida_current:
            partida_activa = u.partida_current.id
            estat = u.partida_current.estat
        else:
            partida_activa = '-'
            estat = 'INACTIVE'

        # Jocs registrats
        jr_count = 0
        if u.date_register_game1: jr_count += 1
        if u.date_register_game2:jr_count += 1
        if u.date_register_game3: jr_count += 1
        if u.date_register_game4: jr_count += 1

        # Jocs finalitzats
        jf_count = 0
        if u.date_end_game1: jf_count += 1
        if u.date_end_game2:jf_count += 1
        if u.date_end_game3: jf_count += 1
        if u.date_end_game4: jf_count += 1

        # Diners guanyats
        if u.game1: game1 = str(u.game1.id)+' ('+str(int(u.money_game1))+')'
        else: game1='-'
        if u.game2: game2 = str(u.game2.id)+' ('+str(int(u.money_game2))+')'
        else: game2='-'
        if u.game3: game3 = str(u.game3.id)+' ('+str(int(u.money_game3))+')'
        else: game3='-'
        if u.game4: game4 = str(u.game4.id)+' ('+str(int(u.money_game4))+')'
        else: game4='-'

        #Diners totals
        if u.punts_totals: total = u.punts_totals
        else: total = '-'

        user = {'id': u.id,
                'name': u.nickname,
                'estat_user': u.status,
                'session_game': u.session_game,
                'estat': estat,
                'partida_activa': partida_activa,
                'jocs_registrats': jr_count,
                'jocs_finalitzats': jf_count,
                'game1': game1,
                'game2': game2,
                'game3': game3,
                'game4': game4,
                'total': u.punts_totals
                }
        users_all_array.append(user)
    response_data['users_all'] = users_all_array


    #############
    ## Results
    #############

    users_results = User.objects.filter(is_robot = 0).order_by('-updated_at')
    users_results_array = []

    game1_c = 0
    game2_c = 0
    game3_c = 0
    game4_c = 0

    game1_d = 0
    game2_d = 0
    game3_d = 0
    game4_d = 0

    game1_c_gain = 0
    game2_c_gain = 0
    game3_c_gain = 0
    game4_c_gain = 0

    game1_d_gain = 0
    game2_d_gain = 0
    game3_d_gain = 0
    game4_d_gain = 0

    for u in users_results:

        if u.session_game == "standard": u.session_game="Standard"
        elif u.session_game == "interact": u.session_game="Interact"
        elif u.session_game == "voice": u.session_game="Voice"
        elif u.session_game == "wall": u.session_game="Wall"


        # Jocs finalitzats
        num_games = 0
        if u.date_end_game1: num_games += 1
        if u.date_end_game2: num_games += 1
        if u.date_end_game3: num_games += 1
        if u.date_end_game4: num_games += 1

        # Cooperation actions

        if u.game1:
            try:
                prisoners = Prisoner.objects.get(user=u.id, partida=u.game1)

                game1 = str(prisoners.seleccio1)+' ('+str(int(prisoners.gain1))+' pts.)'

                if prisoners.seleccio1 == 'C': game1_c += 1
                if prisoners.seleccio1 == 'D': game1_d += 1

                if prisoners.seleccio1 == 'C': game1_c_gain += int(prisoners.gain1)
                if prisoners.seleccio1 == 'D': game1_d_gain += int(prisoners.gain1)

            except Prisoner.DoesNotExist:
                print 'DoesNotExist'
            except Prisoner.MultipleObjectsReturned:
                print 'MultipleObjectsReturned'


        else: game1='-'

        if u.game2:
            try:
                prisoners = Prisoner.objects.get(user=u.id, partida=u.game2)

                game2 = str(prisoners.seleccio1)+' ('+str(int(prisoners.gain1))+' pts.)'

                if prisoners.seleccio1 == 'C': game2_c += 1
                if prisoners.seleccio1 == 'D': game2_d += 1

                if prisoners.seleccio1 == 'C': game2_c_gain += int(prisoners.gain1)
                if prisoners.seleccio1 == 'D': game2_d_gain += int(prisoners.gain1)

            except Prisoner.DoesNotExist:
                print 'DoesNotExist'
            except Prisoner.MultipleObjectsReturned:
                print 'MultipleObjectsReturned'

        else: game2='-'

        if u.game3:
            try:
                prisoners = Prisoner.objects.get(user=u.id, partida=u.game3)

                game3 = str(prisoners.seleccio1)+' ('+str(int(prisoners.gain1))+' pts.)'

                if prisoners.seleccio1 == 'C': game3_c += 1
                if prisoners.seleccio1 == 'D': game3_d += 1

                if prisoners.seleccio1 == 'C': game3_c_gain += int(prisoners.gain1)
                if prisoners.seleccio1 == 'D': game3_d_gain += int(prisoners.gain1)
            except Prisoner.DoesNotExist:
                print 'DoesNotExist'
            except Prisoner.MultipleObjectsReturned:
                print 'MultipleObjectsReturned'

        else: game3='-'

        if u.game4:
            try:
                prisoners = Prisoner.objects.get(user=u.id, partida=u.game4)

                game4 = str(prisoners.seleccio1)+' ('+str(int(prisoners.gain1))+' pts.)'

                if prisoners.seleccio1 == 'C': game4_c += 1
                if prisoners.seleccio1 == 'D': game4_d += 1

                if prisoners.seleccio1 == 'C': game4_c_gain += int(prisoners.gain1)
                if prisoners.seleccio1 == 'D': game4_d_gain += int(prisoners.gain1)
            except Prisoner.DoesNotExist:
                print 'DoesNotExist'
            except Prisoner.MultipleObjectsReturned:
                print 'MultipleObjectsReturned'

        else: game4='-'


        #Diners totals
        if u.punts_totals: total = u.punts_totals
        else: total = '-'

        cooperate = 0
        defect = 0

        try:
            prisoners = Prisoner.objects.filter(user=u.id)
            cooperate = len([p for p in prisoners if p.seleccio1 == 'C'])
            defect = len([p for p in prisoners if p.seleccio1 == 'D'])

            gain_cooperate = math.fsum([p.gain1 for p in prisoners if p.seleccio1 == 'C'])
            gain_defect = math.fsum([p.gain1 for p in prisoners if p.seleccio1 == 'D'])


        except Prisoner.DoesNotExist:
            print 'DoesNotExist'
        except Prisoner.MultipleObjectsReturned:
            print 'MultipleObjectsReturned'


        user = {'id': u.id,
                'num_games': num_games,
                'game1': game1,
                'game2': game2,
                'game3': game3,
                'game4': game4,
                'C': str(cooperate) +' ('+ str(int(gain_cooperate))+' pts.)',
                'D': str(defect) +' ('+ str(int(gain_defect))+' pts.)',
                'total': gain_cooperate + gain_defect,
                }
        users_results_array.append(user)

    c_actions = game1_c+game2_c+game3_c+game4_c
    d_actions = game1_d+game2_d+game3_d+game4_d

    c_gain = game1_c_gain+game2_c_gain+game3_c_gain+game4_c_gain
    d_gain = game1_d_gain+game2_d_gain+game3_d_gain+game4_d_gain

    if c_actions + d_actions > 0:
        perc_cooperation = (c_actions/float(c_actions+d_actions))*100
        perc_defection = (d_actions/float(c_actions+d_actions))*100
    else:
        perc_cooperation = 0
        perc_defection = 0

    print perc_cooperation

    response_data['users_results'] = users_results_array
    response_data['users_results_totals'] = {'perc_cooperation': perc_cooperation,
                                             'perc_defection': perc_defection,
                                             'c_game1': game1_c,
                                             'c_game2': game2_c,
                                             'c_game3': game3_c,
                                             'c_game4': game4_c,
                                             'd_game1': game1_d,
                                             'd_game2': game2_d,
                                             'd_game3': game3_d,
                                             'd_game4': game4_d,
                                             'c_gain_game1': game1_c_gain,
                                             'c_gain_game2': game2_c_gain,
                                             'c_gain_game3': game3_c_gain,
                                             'c_gain_game4': game4_c_gain,
                                             'd_gain_game1': game1_d_gain,
                                             'd_gain_game2': game2_d_gain,
                                             'd_gain_game3': game3_d_gain,
                                             'd_gain_game4': game4_d_gain,
                                             'c_gain': c_gain,
                                             'd_gain': d_gain}




    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def stats_partida(request, **kwargs):
    print 'Stats'

@csrf_exempt
def stats_partida_detail(request, **kwargs):

    id = kwargs.get('num_partida', None)

    partida = Partida.objects.filter(id=id)[0]


    users = []
    if partida.classe == 'standard':
        users = User.objects.filter(gam1=partida)

    if partida.classe == 'interact':
        users = User.objects.filter(game2=partida)

    if partida.classe == 'voice':
        users = User.objects.filter(game3=partida)

    if partida.classe == 'wall':
        users = User.objects.filter(game4=partida)

    error = ""
    if partida.estat == 'ACABADA' or partida.estat == 'ACABADA_MANUAL':
        if partida.data_creacio is None:
            error = error + 'ERROR 301: La partida no sha creat.'
            error = error + '\n'
        if partida.data_inicialitzacio is None:
            error = error + 'ERROR 302: La partida no sha iniciat.'
            error = error + '\n'
        if partida.data_finalitzacio is None:
            error = error + 'ERROR 303: La partida no sha acabat.'
            error = error + '\n'
    elif partida.estat == 'REGISTRANT':
        if partida.usuaris_registrats == 0:
            error = error + 'ERROR 304: No hi ha cap usuari a la partida'
            error = error + '\n'
        if partida.usuaris_registrats == 2:
            error = error + 'ERROR 305: La partida tendria que estar jugant-se'
            error = error + '\n'
    elif partida.estat == 'JUGANT':
        if partida.usuaris_registrats == 0:
            error = error + 'ERROR 306: No hi ha jugadors a la partida'
            error = error + '\n'
        if partida.usuaris_registrats == 1:
            error = error + 'ERROR 307: Falta un jugador a la partida'
            error = error + '\n'

    print error

    response_data = {
        "id": partida.id,
        "num_partida": partida.num_partida,
        "creacio": (partida.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if partida.data_creacio else '-',
        "inici": (partida.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if partida.data_inicialitzacio else '-',
        "fin": (partida.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if partida.data_finalitzacio else '-',
        "estat": partida.estat,
        "classe": partida.classe,
        "users": [u.id for u in users] if len(users) > 0 else '-',
        "error": error
    }


    return HttpResponse(json.dumps(response_data), content_type="application/json")


###############################################################################################
##################################         ANALYSIS      ######################################
###############################################################################################

@csrf_exempt
def basic_analysis(request, **kwargs):
    participants = User.objects.filter(is_robot=0)
    prisoners = Prisoner.objects.filter()

    response_participants = {
        "number_of_participants": len(participants) if participants else 0,
    }

    c_exp_standard = [p for p in prisoners if p.partida.classe == 'standard' and p.guess1 == 'C']
    d_exp_standard = [p for p in prisoners if p.partida.classe == 'standard' and p.guess1 == 'D']
    c_standard = [p for p in prisoners if p.partida.classe == 'standard' and p.seleccio1 == 'C']
    d_standard = [p for p in prisoners if p.partida.classe == 'standard' and p.seleccio1 == 'D']


    response_standard = {
        "cooperation_expected_standard" : len(c_exp_standard) if c_exp_standard else 0,
        "defection_expected_standard" : len(d_exp_standard) if d_exp_standard else 0,
        "cooperation_standard" : len(c_standard) if c_standard else 0,
        "defection_standard" : len(d_standard) if d_standard else 0,
    }


    c_exp_interact = [p for p in prisoners if p.partida.classe == 'interact' and p.guess1 == 'C']
    d_exp_interact = [p for p in prisoners if p.partida.classe == 'interact' and p.guess1 == 'D']
    c_interact = [p for p in prisoners if p.partida.classe == 'interact' and p.seleccio1 == 'C']
    d_interact = [p for p in prisoners if p.partida.classe == 'interact' and p.seleccio1 == 'D']

    response_interact = {
        "cooperation_expected_interact" : len(c_exp_interact) if c_exp_interact else 0,
        "defection_expected_interact" : len(d_exp_interact) if d_exp_interact else 0,
        "cooperation_interact" : len(c_interact) if c_interact else 0,
        "defection_interact" : len(d_interact) if d_interact else 0,
    }
    
    c_exp_voice = [p for p in prisoners if p.partida.classe == 'voice' and p.guess1 == 'C']
    d_exp_voice = [p for p in prisoners if p.partida.classe == 'voice' and p.guess1 == 'D']
    c_voice = [p for p in prisoners if p.partida.classe == 'voice' and p.seleccio1 == 'C']
    d_voice = [p for p in prisoners if p.partida.classe == 'voice' and p.seleccio1 == 'D']

    response_voice = {
        "cooperation_expected_voice" : len(c_exp_voice) if c_exp_voice else 0,
        "defection_expected_voice" : len(d_exp_voice) if d_exp_voice else 0,
        "cooperation_voice" : len(c_voice) if c_voice else 0,
        "defection_voice" : len(d_voice) if d_voice else 0,
    }
    
    c_exp_wall = [p for p in prisoners if p.partida.classe == 'wall' and p.guess1 == 'C']
    d_exp_wall = [p for p in prisoners if p.partida.classe == 'wall' and p.guess1 == 'D']
    c_wall = [p for p in prisoners if p.partida.classe == 'wall' and p.seleccio1 == 'C']
    d_wall = [p for p in prisoners if p.partida.classe == 'wall' and p.seleccio1 == 'D']

    response_wall = {
        "cooperation_expected_wall" : len(c_exp_wall) if c_exp_wall else 0,
        "defection_expected_wall" : len(d_exp_wall) if d_exp_wall else 0,
        "cooperation_wall" : len(c_wall) if c_wall else 0,
        "defection_wall" : len(d_wall) if d_wall else 0,
    }


    # Cooperation vs Cooperation

    coordination_cooperate = 0
    coordination_defect = 0
    anti_coordination = 0

    for p1 in prisoners:
        for p2 in prisoners:
            if p1.partida == p2.partida and p1.rival1_id==p2.user_id:
                if p1.seleccio1 == 'C' and p2.seleccio1 =='C':
                    coordination_cooperate += 1
                elif p1.seleccio1 == 'D' and p2.seleccio1 =='D':
                    coordination_defect += 1
                elif p1.seleccio1 == 'D' and p2.seleccio1 =='C' or p1.seleccio1 == 'C' and p2.seleccio1 =='D':
                    anti_coordination += 1


    response_strategies = {
        "coordination_cooperate": coordination_cooperate/2,
        "coordination_defect": coordination_defect/2,
        "anti_coordination": anti_coordination/2
    }
   
    response_data = {
        "participants": response_participants,
        "standard": response_standard,
        "interact": response_interact,
        "voice": response_voice,
        "wall": response_wall,
        "strategies": response_strategies,
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")



from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import *

from django import forms
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils import timezone

from game.models import *
from game.vars import *

import math

import random

def user_exists_in_db(user):
    try:
        User.objects.get(pk=user.id)
        return True
    except:
        return False

def index(request, **kwargs):
    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        print user.email
        return redirect('user.registre')

    return redirect('user.nickname')

#########################################################################################################
#########################################################################################################
# Pantalla 1: Escollir un nickname
class NicknameForm(forms.Form):
    nickname = forms.CharField(max_length=300)

@csrf_exempt
def nickname(request, **kwargs):
    if not('game' in request.session) or request.session['game'] is None:
        print 'ERROR 107: Seleccionar Joc'
        #user = request.session['user']
        #if not user_exists_in_db(user):
        #    del request.session['user']
        #    return redirect('user.nickname')
        return redirect('index')

    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        return redirect('user.registre')

    #Borrem el nickanme de la sessio
    if 'nickname' in request.session:
        del request.session['nickname']

    if request.method != 'POST':
        return render_to_response('nickname.html', {'lang': request.session['lang'], 'game': request.session['game'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))
    else:
        form = NicknameForm(request.POST)
        nick = form['nickname'].value()

        if not nick or len(nick) == 0:
            return render_to_response('nickname.html', {'lang': request.session['lang'], 'game': request.session['game'], 'text': request.session['text']},
                                      context_instance=RequestContext(request))

        if len(nick) > 20:
            return render_to_response('nickname.html',
                                      {'nickname_error': False, 'nickname_error2': True, 'nickname': nick,
                                       'lang': request.session['lang'], 'text': request.session['text'], 'game': request.session['game']},
                                      context_instance=RequestContext(request))

        #Si l'usuari ja existeix enviar-lo a la pantalla d'inici
        try:
            user = User.objects.get(nickname=nick)
            if user.partida_current:
                if user.partida_current.classe != request.session['game']: # Usuari amb partida activa que no es la que intenta accedir
                    user.status = "Error - Nickname"
                    user.save()
                    return render_to_response('nickname.html',
                                      {'nickname_error1': True,
                                       'nickname_error2': False,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            if user.date_end_game1 and request.session['game']=="standard": # El participant ja ha jugat aquest joc
                user.status = "Error - Nickname"
                user.save()
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            elif user.date_end_game2 and request.session['game']=="interact": # El participant ja ha jugat aquest joc
                user.status = "Error - Nickname"
                user.save()
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            elif user.date_end_game3 and request.session['game']=="voice": # El participant ja ha jugat aquest joc
                user.status = "Error - Nickname"
                user.save()
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            elif user.date_end_game4 and request.session['game']=="wall": # El participant ja ha jugat aquest joc
                user.status = "Error - Nickname"
                user.save()
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            else:
                user = User.objects.get(nickname=nick)
                user.session_game = request.session['game']
                user.status = "Register"
                user.save()

                request.session['user'] = user
                request.session['nickname'] = nick
                return redirect('user.registre')

        #Sino enviar-lo a l'enquesta
        except ObjectDoesNotExist:
            request.session['user'] = None
            request.session['nickname'] = nick

            return redirect('user.avis')

#########################################################################################################
#########################################################################################################
# Pantalla avis legal
class AvisForm(forms.Form):
    check_1 = forms.CharField(max_length=20)

@csrf_exempt
def avis(request, **kwargs):
    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.login')
        #print user.useremail_set.all()
        return redirect('user.inici')


    if request.method != 'POST':
        return render_to_response('avis.html',  {'lang': request.session['lang'], 'text': request.session['text']},
                              context_instance=RequestContext(request))
    else:
        form = AvisForm(request.POST)
        request.session['check1'] = True

        return redirect('user.enquesta1')

#########################################################################################################
#########################################################################################################
# Pantalla 5: Enquesta 1
class SigninForm1(forms.Form):
    genere = forms.CharField(max_length=100)
    rang_edat = forms.CharField(max_length=100)
    on_vius = forms.CharField(max_length=6)

@csrf_exempt
def enquesta1(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        # print user.useremail_set.all()
        return redirect('user.registre')

    # Ens assegurem que tenim l'email almenys
    if 'nickname' not in request.session or request.session['nickname'] is None:
        print "ERROR!!"
        return redirect('user.nickname')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquesta1.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'game': request.session['game']},
                                  context_instance=RequestContext(request))

    form = SigninForm1(request.POST)
    genere = form['genere'].value()
    rang_edat = form['rang_edat'].value()
    on_vius = form['on_vius'].value()

    if not form.is_valid():
        return render_to_response('enquesta1.html', {
            'genere': genere,
            'genere_danger': genere is None or len(genere) == 0,
            'genere_1_checked': 'bx-option-selected' if genere == 'F' else '',
            'genere_2_checked': 'bx-option-selected' if genere == 'M' else '',
            'genere_3_checked': 'bx-option-selected' if genere == 'T' else '',
            'genere_4_checked': 'bx-option-selected' if genere == 'O' else '',
            'genere_5_checked': 'bx-option-selected' if genere == 'N' else '',

            'rang_edat': rang_edat,
            'rang_edat_danger': rang_edat is None or len(rang_edat) == 0,
            'rang_edat_1_checked': 'bx-option-selected' if rang_edat == 'r1' else '',
            'rang_edat_2_checked': 'bx-option-selected' if rang_edat == 'r2' else '',
            'rang_edat_3_checked': 'bx-option-selected' if rang_edat == 'r3' else '',
            'rang_edat_4_checked': 'bx-option-selected' if rang_edat == 'r4' else '',
            'rang_edat_5_checked': 'bx-option-selected' if rang_edat == 'r5' else '',
            'rang_edat_6_checked': 'bx-option-selected' if rang_edat == 'r6' else '',

            'on_vius': on_vius,
            'on_vius_danger': on_vius is None or len(on_vius) == 0,
            'on_vius_1_checked': 'bx-option-selected' if on_vius == 'r1' else '',
            'on_vius_2_checked': 'bx-option-selected' if on_vius == 'r2' else '',
            'on_vius_3_checked': 'bx-option-selected' if on_vius == 'r3' else '',
            'lang': request.session['lang'],
            'text': request.session['text'],
            'game': request.session['game']},
            context_instance=RequestContext(request))

    else:


        request.session['genere'] = genere
        request.session['rang_edat'] = rang_edat
        request.session['on_vius'] = on_vius

        user = User()

        user.nickname = request.session['nickname']
        user.genere = request.session['genere']
        user.on_vius = request.session['on_vius']
        user.rang_edat = request.session['rang_edat']
        user.check1 = request.session['check1']


        user.data_creacio = timezone.localtime(timezone.now())

        user.status = "Survey-1"
        user.session_game = request.session['game']

        user.save()

        request.session['user'] = user

        return redirect('user.registre')

#########################################################################################################
#########################################################################################################
@csrf_exempt
def logout(request, **kwargs):
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        user.status = "Logged-Out"

        if user.partida_current:
            user.partida_current = None

        user.save()
        del request.session['user']
    return redirect('index')

#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################

#Pantalla 2:Seleccio de l'experiment si ja hi ha un usuari a la sessio
@csrf_exempt
def inici(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.nickname')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Mirem que aquest user no hagi acabat ja!!!
    if user.data_finalitzacio:
        return redirect('user.final_joc')

    # si l'usuari no te cap partida assignada
    if not user.partida:
        #Mirem si ens estan demanant d'entrar a partida o encara no
        if request.method != 'POST':
            return render_to_response('inici.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False},
                                      context_instance=RequestContext(request))

        # Si demanem entrar a partida, primer mirem si n'hi ha una d'activa
        partida_activa = Partida.objects.filter(estat="REGISTRANT")
        if len(partida_activa) > 0:
            # Si es aixi registrem a l'usuari
            partida_activa = partida_activa[0]
            #print partida_activa.num_partida

            try:
                #Controlem que nomes hi hagi 6 usuaris a la partida!!
                if partida_activa.usuaris_registrats < 6:
                    partida_activa.usuaris_registrats += 1
                    partida_activa.save()
                    print "Partida", partida_activa.num_partida,"// usuaris registrats:", partida_activa.usuaris_registrats

                    user.partida = partida_activa
                    user.data_registre = timezone.localtime(timezone.now())
                    user.save()
                else:
                    return redirect('user.inici')

                #Si tot ha sortit be, redirigim l'usuari a la pantalla de joc
                return redirect('game.index')
            except:
                #Si hi ha hagut error tornem a la pagina
                return redirect('user.inici')


        return render_to_response('inici.html', {'user': user,
                                                 'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'error_partida':True},
                                  context_instance=RequestContext(request))

    # Si l'usuari te partida assignada
    else:
        #Si l'usuari ja te una partida assignada i aquesta encara esta registrant
        if user.partida and user.partida.estat == "REGISTRANT":
            return redirect('game.index')


        #Si l'usuari ja te una partida assignada i aquesta no ha comensat a jugar
        if user.partida and user.partida.estat == "JUGANT":
            date_now = timezone.localtime(timezone.now())
            date_start = user.partida.data_inicialitzacio
            temps_actual_joc = (date_now - date_start).total_seconds()

            #print date_now, date_start, temps_actual_joc, TEMPS_INICI_SEC
            if temps_actual_joc < TEMPS_INICI_SEC:
                return redirect('game.index')

            else :
                 #return redirect('game.index')
                return redirect('user.inici')


        #Si la partida on ha participat l'usuari ja esta acabada, l'envio als resultats
        if user.partida and (user.partida.estat == "ACABADA" or user.partida.estat == "ACABADA_MANUAL"):
            return redirect('user.final_joc')

        return redirect('user.inici')

#####################################################################################################
########################################### REGISTRE ################################################
#####################################################################################################

@csrf_exempt
def registre(request, **kwargs):

    print request.session['game']

    ## User without session
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.nickname')
    ## Update the user information of the session
    try:
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    ## Get the games is "REGISTRANT"
    partida_activa = Partida.objects.filter(estat="REGISTRANT").filter(classe=request.session["game"])
    ## Get the fist game is "REGISTRANT"
    if len(partida_activa) > 0:
        partida_activa = partida_activa[0]

    ## User without ACTIVE GAME
    if not user.partida_current:
        print 'x0001x User with NO ACTIVE GAME'
        ## POST to ENTER in the GAME
        if request.method != 'POST':
            print 'x0002x NO POST'
            return render_to_response('registre.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False,
                                                     'game': request.session['game'],
                                                     'waiting':0},
                                      context_instance=RequestContext(request))

        ## ACTIVE GAME
        if partida_activa:
            print 'x0002x Active Game'
            try:
                ## Max. 2 users in the game
                if partida_activa.usuaris_registrats < 2:
                    partida_activa.usuaris_registrats += 1
                    partida_activa.save()

                    ## Assigning GAME to CURRENT GAME
                    user.partida_current = partida_activa

                    ## Assigning TIME to REGISTER
                    if request.session['game'] == "standard": user.date_register_game1 = timezone.localtime(timezone.now())
                    if request.session['game'] == "interact": user.date_register_game2 = timezone.localtime(timezone.now())

                    ## Assigning GAME to USER
                    if request.session['game'] == "standard": user.game1 = partida_activa
                    if request.session['game'] == "interact": user.game2 = partida_activa


                    user.status = "Register-Waiting"
                    user.session_game = request.session['game']
                    user.save()

                ## Get ALL USERS in with the CURRENT ACTIVE GAME
                if request.session['game'] == "standard": usuaris = User.objects.filter(game1=partida_activa)
                if request.session['game'] == "interact": usuaris = User.objects.filter(game2=partida_activa)

                ## With 2 USERS we generate the GAME
                if (len(usuaris) > 1):
                    partida_activa.estat = "GENERANT_DADES"
                    partida_activa.save()

                    if request.session['game'] == "standard": generar_prisoner(usuaris, partida_activa)
                    if request.session['game'] == "interact": generar_prisoner(usuaris, partida_activa)

                return redirect('user.registre')

            except:
                ## Error in the creation of the game
                print 'x0003x Exception Game Creation'
                return redirect('user.registre')

        ## Creation of a NEW GAME
        else:
            print 'x0004x New Active Game'
            ## Number Next Game
            results = Partida.objects.all().order_by('-num_partida')
            npartida = 1
            if len(results) > 0:
                npartida = results[0].num_partida+1

            ## Create new Game
            partida = Partida.objects.create(num_partida=npartida,
                                     data_creacio=timezone.localtime(timezone.now()),
                                     estat="REGISTRANT",
                                     classe=request.session["game"])
            partida.save()

            ## Assigning GAME to CURRENT GAME
            user.partida_current = partida

            ## Assigning TIME to REGISTER
            if request.session['game'] == "standard": user.date_register_game1 = timezone.localtime(timezone.now())
            if request.session['game'] == "interact": user.date_register_game2 = timezone.localtime(timezone.now())
            if request.session['game'] == "voice": user.date_register_game3 = timezone.localtime(timezone.now())
            if request.session['game'] == "wall": user.date_register_game4 = timezone.localtime(timezone.now())

            ## Assigning GAME to USER
            if request.session['game'] == "standard": user.game1 = user.partida_current
            if request.session['game'] == "interact": user.game2 = user.partida_current
            if request.session['game'] == "voice": user.game3 = user.partida_current
            if request.session['game'] == "wall": user.game4 = user.partida_current


            user.data_last_action = timezone.localtime(timezone.now())
            user.status = "Register-Creating"
            user.session_game = request.session['game']
            user.save()

            ## VOICE prisoner
            if request.session['game'] == "voice":
                print 'x0005x Create Voice Game'
                partida_activa.estat = "GENERANT_DADES"
                partida.usuaris_registrats += 1

            ## WALL prisoner
            if request.session['game'] == "wall":
                print 'x0005x Create Wall Game'
                partida_activa.estat = "GENERANT_DADES"
                rival = pop_resident()
                partida.usuaris_registrats += 1

            partida.usuaris_registrats += 1
            partida.save()

            #ToDo: chapucilla amb el redirect
            # VOICE prisoner
            if request.session['game'] == "voice":
                generar_prisoner([user], partida)
                return redirect('user.joc_prisoner1_1')

            # WALL prisoner
            if request.session['game'] == "wall":
                generar_prisoner([user, rival], partida)
                return redirect('user.joc_prisoner1_1')


        print 'x0100x Go To RENDER'
        return render_to_response('registre.html', {'user': user,
                                                    'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                    'error_partida':False,
                                                    'game': request.session['game'],
                                                    'waiting':1},
                                                    context_instance=RequestContext(request))
    ## User with ACTIVE GAME
    else:
        print 'x0006x User with ACTIVE GAME'
        print '--------------------------'
        print 'Partida Activa: ' +str(user.partida_current.id)
        print 'Partida Activa Status: ' +str(user.partida_current.estat)
        print 'Partida Activa Session: '+str(user.partida_current.classe)
        print 'Game Session: '+str(request.session['game'])
        print '--------------------------'

        if user.partida_current.classe != request.session['game']:
            return render_to_response('registre.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False,
                                                     'error_partida_2':True, # partida_activa
                                                     'game': request.session['game'],
                                                     'waiting':0},
                                      context_instance=RequestContext(request))

        print 'x0008x User with ACTIVE GAME'

        # Game Finished
        if user.partida_current and (user.partida_current.estat == "ACABADA" or user.partida_current.estat == "ACABADA_MANUAL"):
            return redirect('user.final_joc')

        # Game Playing
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "standard":
            return redirect('user.joc_prisoner1_1')
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "interact":
            return redirect('user.joc_prisoner1_1')
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "voice":
            return redirect('user.joc_prisoner1_1')
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "wall":
            return redirect('user.joc_prisoner1_1')

        # Registering
        if user.partida_current and (user.partida_current.estat == "REGISTRANT"):
            # Agafam els usuaris
            if request.session['game'] == "standard": usuaris = User.objects.filter(game1=partida_activa)
            if request.session['game'] == "interact": usuaris = User.objects.filter(game2=partida_activa)
            if request.session['game'] == "voice": usuaris = User.objects.filter(game3=partida_activa)
            if request.session['game'] == "wall": usuaris = User.objects.filter(game4=partida_activa)

            # Games Standard and Interact
            if (len(usuaris) > 1):
                partida_activa.estat = "GENERANT_DADES"
                partida_activa.save()

                if request.session['game'] == "standard": generar_prisoner(usuaris, partida_activa)
                if request.session['game'] == "interact": generar_prisoner(usuaris, partida_activa)

            # Games Voice and Wall
            if (len(usuaris) == 1):
                partida_activa.estat = "GENERANT_DADES"
                partida_activa.save()

                if request.session['game'] == "voice": generar_prisoner(usuaris, partida_activa)
                if request.session['game'] == "wall": generar_prisoner([user, rival], partida_activa)

        print 'x0008x Refreshing'
        # Refreshing
        return render_to_response('registre.html', {'user': user,
                                                    'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                    'error_partida':False,
                                                    'game': request.session['game'],
                                                    'waiting':1},
                                  context_instance=RequestContext(request))


#####################################################################################################
###################################### GENERACIO DE DADES ###########################################
#####################################################################################################

def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

def pop_resident():

    resident = Resident.objects.all().order_by("last_selected")[0]

    resident.last_selected = timezone.localtime(timezone.now())
    resident.save()

    return resident

#####################################################################################################
###################################### GENERACIO DE DICTATOR ########################################
#####################################################################################################

def generar_prisoner(usuaris, partida_activa):


    print 'x0010x Generar Prisoner'

    game_prisoner = []

    ################
    #### Wall ######
    ################

    if partida_activa.classe == 'wall':
        prisoner = Prisoner()
        prisoner.user = usuaris[0]
        prisoner.partida = partida_activa
        game_prisoner.append(prisoner)
        prisoner.save()

        usuaris[0].num_jugador = 1
        usuaris[0].save()

        game_prisoner[0].rol1 = 'E'
        game_prisoner[0].seleccio1 = ''
        game_prisoner[0].rival1_resident = usuaris[1]
        game_prisoner[0].save()

    ################
    #### Voice #####
    ################

    elif partida_activa.classe == 'voice':
        prisoner = Prisoner()
        prisoner.user = usuaris[0]
        prisoner.partida = partida_activa
        game_prisoner.append(prisoner)
        prisoner.save()

        usuaris[0].num_jugador = 1
        usuaris[0].save()

        game_prisoner[0].rol1 = 'E'
        game_prisoner[0].seleccio1 = ''
        game_prisoner[0].save()



    else:
        ################################
        #### Standard and Interact #####
        ################################

        for i in range(len(usuaris)):

            prisoner = Prisoner()
            prisoner.user = usuaris[i]
            prisoner.partida = partida_activa
            game_prisoner.append(prisoner)
            prisoner.save()

        # Assignem un numero als participants de l'experiment
        random.shuffle(NUMS_JUGADOR)
        # Prisoner Game - Valors inicials
        random.shuffle(ADVANTAGE_DISADVANTAGE)

        # Prisoner Dilemma - Llistat usuaris
        llista_prisoner1 = [] # JUGADORES IGUALES


        for i in range(len(usuaris)):
            # Numero de jugador per cada usuari
            usuaris[i].num_jugador = NUMS_JUGADOR[i]

            # Cream les dades per cas Prisoner 1
            if partida_activa.classe == 'standard' or partida_activa.classe == "interact":
                game_prisoner[i].rol1 = 'E'
                llista_prisoner1.append(game_prisoner[i])

            usuaris[i].save()

        #Fem les parelles al Prisoner
        if partida_activa.classe == 'standard' or partida_activa.classe == "interact":
            while llista_prisoner1:
                rand1_prisoner = pop_random(llista_prisoner1)
                rand2_prisoner = pop_random(llista_prisoner1)
                rand1_prisoner.rival1 = rand2_prisoner.user
                rand2_prisoner.rival1 = rand1_prisoner.user
                rand1_prisoner.save()
                rand2_prisoner.save()

    partida_activa.estat = "JUGANT"
    partida_activa.data_inicialitzacio = timezone.localtime(timezone.now())
    partida_activa.save()

    print 'x0011x Generated Prisoner'
    return


######################################################################################
################################### PRISONER 1 #######################################
######################################################################################

@csrf_exempt
def joc_prisoner1_1(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.joc_prisoner1_2')
        else:
            return redirect('user.logout')

    user.status = "Playing-"+request.session['game']+"-I"
    user.session_game = request.session['game']
    user.save()

    # Send the name of the rival in Wall
    rival_name = ''
    if request.session['game'] == 'wall': rival_name = user_prisoner.rival1_resident.name

    return render_to_response('joc_prisoner1_1.html', {'lang': request.session['lang'],
                                                       'text': request.session['text'],
                                                       'user': request.session['user'],
                                                       'rival': rival_name,
                                                       'matrix': MATRIX1},
                              context_instance=RequestContext(request))

@csrf_exempt
def joc_prisoner1_2(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.joc_prisoner1_3')
        else:
            return redirect('user.logout')

    user.session_game = request.session['game']
    user.status = "Playing-"+request.session['game']+"-II"
    user.save()

    # Send the name of the rival in Wall
    rival_name = ''
    if request.session['game'] == 'wall': rival_name = user_prisoner.rival1_resident.name

    return render_to_response('joc_prisoner1_2.html', {'lang': request.session['lang'],
                                                       'text': request.session['text'],
                                                       'user': request.session['user'],
                                                       'rival': rival_name,
                                                       'matrix': MATRIX1},
                              context_instance=RequestContext(request))

@csrf_exempt
def joc_prisoner1_3(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.final_joc')
        else:
            return redirect('user.logout')

    user.status = "Playing-"+request.session['game']+"-III"
    user.session_game = request.session['game']
    user.save()

    # Send the name of the rival in Wall
    rival_name = ''
    if request.session['game'] == 'wall': rival_name = user_prisoner.rival1_resident.name


    return render_to_response('joc_prisoner1_3.html', {'lang': request.session['lang'],
                                                       'text': request.session['text'],
                                                       'user': request.session['user'],
                                                       'rival': rival_name,
                                                       'matrix': MATRIX1},
                              context_instance=RequestContext(request))


@csrf_exempt
def final_joc(request, **kwargs):

    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.logout')

    # TANCA LA PARTIDA

    # Miramos si los dos usuarios de la partida han finalizado la sesion


    if request.session['game'] == "standard":user.date_end_game1 = timezone.localtime(timezone.now())
    if request.session['game'] == "interact":user.date_end_game2 = timezone.localtime(timezone.now())
    if request.session['game'] == "voice":user.date_end_game3 = timezone.localtime(timezone.now())
    if request.session['game'] == "wall":user.date_end_game4 = timezone.localtime(timezone.now())

    user.status = "Finishing"
    user.session_game = request.session['game']
    user.save()

    user.save()

    # Agafam els usuaris
    if request.session['game'] == "standard": usuaris = User.objects.filter(game1=user.partida_current)
    if request.session['game'] == "interact": usuaris = User.objects.filter(game2=user.partida_current)
    if request.session['game'] == "voice": usuaris = User.objects.filter(game3=user.partida_current)
    if request.session['game'] == "wall": usuaris = User.objects.filter(game4=user.partida_current)

    num_usuaris_acabats = 0

    print "usuaria a la partida: " +str(len(usuaris))
    for u in usuaris:
        if request.session['game'] == "standard" and u.date_end_game1:
            num_usuaris_acabats = num_usuaris_acabats + 1
        if request.session['game'] == "interact" and u.date_end_game2:
            num_usuaris_acabats = num_usuaris_acabats + 1
        if request.session['game'] == "voice" and u.date_end_game3:
            num_usuaris_acabats = num_usuaris_acabats + 1
        if request.session['game'] == "wall" and u.date_end_game4:
            num_usuaris_acabats = num_usuaris_acabats + 1

    print 'numero de usuaris: '+ str(num_usuaris_acabats)
    if num_usuaris_acabats == 2:
        user.partida_current.data_finalitzacio = timezone.localtime(timezone.now())
        user.partida_current.estat = "ACABADA"
        user.partida_current.save()

    if num_usuaris_acabats == 1 and request.session['game'] == "voice":
        user.partida_current.data_finalitzacio = timezone.localtime(timezone.now())
        user.partida_current.estat = "ACABADA"
        user.partida_current.save()

    if num_usuaris_acabats == 1 and request.session['game'] == "wall":
        user.partida_current.data_finalitzacio = timezone.localtime(timezone.now())
        user.partida_current.estat = "ACABADA"
        user.partida_current.save()

    user.partida_current = None

    user.status = ""
    user.session_game = ""
    user.save()

    user.save()

    #Todo: Vigilar si aixo es necessari
    #del request.session['user']
    #del request.session['game']

    resultats = [user.money_game1, user.money_game2, user.money_game3, user.money_game4]

    finalitzats = []

    if user.date_end_game1: finalitzats.append(1)
    else: finalitzats.append(0)

    if user.date_end_game2: finalitzats.append(1)
    else: finalitzats.append(0)

    if user.date_end_game3: finalitzats.append(1)
    else: finalitzats.append(0)

    if user.date_end_game4: finalitzats.append(1)
    else: finalitzats.append(0)

    return render_to_response('final_joc.html', {'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'max': [TOTAL_MAX1, TOTAL_MAX2, TOTAL_MAX3, TOTAL_MAX4],
                                                 'resultats': resultats,
                                                 'finalitzats': finalitzats,
                                                 'vals': 0,
                                                 'nickname': user.nickname,
                                                 'game': request.session['game'],
                                                 },
                              context_instance=RequestContext(request))
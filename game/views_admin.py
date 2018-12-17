from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django import forms

from game.models import *
from django.shortcuts import redirect
import random
from django.utils import timezone

from game.vars import *

import datetime

random.seed(datetime.datetime.now())



def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

@csrf_exempt
def registre(request, **kwargs):
    print('Registre en el cas que noltros arrenquem sa partida')
    print('Codi de creacio de partida')
    print('Codi per quan tenim el registre obert')

    return render_to_response('admin_registre.html', {'lang': request.session['lang'],
                                                      'pagina': 'registre',
                                                      'text': request.session['text']},
                              context_instance=RequestContext(request))

@csrf_exempt
def partida(request, **kwargs):
    #Si no hi ha partida jugant-se mostrar avis
    return render_to_response('admin_partida.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'partida',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

@csrf_exempt
def partida_list(request, **kwargs):

    return render_to_response('admin_partida_list.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'partida',
                                         'text': request.session['text']},
                              context_instance=RequestContext(request))

@csrf_exempt
def partida_detail(request, **kwargs):
    num_partida = kwargs.get('num_partida', None)

    #Si no hi ha partida jugant-se mostrar avis
    return render_to_response('admin_partida_detail.html', {
                                         'lang': request.session['lang'],
                                         'num_partida': num_partida,
                                         'pagina': 'partida',
                                         'text': request.session['text']},
                                        context_instance=RequestContext(request))

@csrf_exempt
def stats(request, **kwargs):
    #Sino es un post, ensenyem el boto per crear registre nou
    return render_to_response('admin_stats.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'stats',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

@csrf_exempt
def users(request, **kwargs):

    return render_to_response('admin_users.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'users',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

@csrf_exempt
def results(request, **kwargs):

    return render_to_response('admin_results.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'results',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

@csrf_exempt
def users_list(request, **kwargs):

    return render_to_response('admin_users_list.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'users',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))


@csrf_exempt
def users_results(request, **kwargs):

    return render_to_response('admin_users_results.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'users_results',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

@csrf_exempt
def users_reset(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    print "Reseting user", user_id
    if user_id is not None:
        user = User.objects.get(id=user_id)
        if user is not None:
            user.partida=None
            user.save()
    return redirect('admin.users')





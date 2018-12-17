from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from game.models import User
from game.vars import *

from game.views_user import user_exists_in_db
from django.utils import timezone

from django import forms


@csrf_exempt
def index(request, **kwargs):

    print 'Game Index'

@csrf_exempt
def presentacio(request, **kwargs):

    if not('game' in request.session) or request.session['game'] is None:
        print 'ERROR 107: Seleccionar Joc'
        return redirect('index')

    return render_to_response('presentacio.html', {'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                    'game': request.session['game']})








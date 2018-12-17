from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request, **kwargs):

    if 'user' in request.session:
        del request.session['user']
    if 'game' in request.session:
        del request.session['game']

    return render_to_response('index.html', {'lang': request.session['lang'],
                                             'text': request.session['text']},
							  context_instance=RequestContext(request))


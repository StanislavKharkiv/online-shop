from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template.loader import render_to_string

# Create your views here.

def user_index(request):
    t = render_to_string('user/index.html')
    return HttpResponse(t)

def user_info(request, id):
    print(request.GET)
    if id > 99: 
        raise Http404()
    if id == 0:
        return redirect('/user/')
    
    return HttpResponse(render_to_string('user/user.html', {'id': id}))
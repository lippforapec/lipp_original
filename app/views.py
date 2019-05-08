from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

data = [{'id': 1, 'name': 'startup1'}, {'id':2, 'name': 'startup2'}]

def startup_index(request):
    context = {
        'startups': data
    }
    return render(request, 'startups/index.html', data)

def startup_show(request, id):
    context = { 'startup': list(filter(lambda s: s['id'] == id, data)) }
    return render(request, 'startups/show.html', context)

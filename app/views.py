from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.forms.models import model_to_dict

from .forms import StartupForm, SimpleStartupForm
from .models import Startup

def main(request):
    return render(request, 'main.html')

def startup_index(request):
    context = {
        'watching': Startup.objects.all()[:3],
        'trending': Startup.objects.all(),
        'technology': Startup.objects.all(),# filter(category=24),
    }
    return render(request, 'startups/index.html', context)

def startup_show(request, id):
    context = { 'startup': Startup.objects.filter(id = id).first() }
    return render(request, 'startups/show.html', context)

# form: https://tutorial.djangogirls.org/ko/django_forms/
def startup_new(request):
    if request.method == "POST":
        form = StartupForm(request.POST)
        if form.is_valid():
            startup = form.save(commit=False)
            startup.user = request.user
            #startup.created_at = timezone.now()
            startup.save()
            return redirect('startup_show', id=startup.id)
    else:
        form = StartupForm()
    return render(request, 'startups/new.html', {'form': form})

def startup_edit(request, id):
    startup = Startup.objects.get(id = id)
    sd = model_to_dict(startup)
    if request.method == "POST":
        form = SimpleStartupForm(request.POST, instance = startup)
        if form.is_valid():
            form.save()
            return redirect('startup_show', id = startup.id)
        else:
            print(form.errors)
            return render(request, 'startups/edit.html', {'form': StartupForm(initial=sd), 'id': startup.id, 'errors': form.errors})
    else:
        sd['tags'] = sd['tags'].replace("[","").replace("\"","").replace("]","")
    return render(request, 'startups/edit.html', {'form': StartupForm(initial=sd), 'id': startup.id})

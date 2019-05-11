<<<<<<< HEAD
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
=======
from django.shortcuts import render, redirect
from django.http import HttpResponse
>>>>>>> 6fe9bec7cc0be2c0ae2e54ef251c840ddd63e469
from django.views import generic
from django.forms.models import model_to_dict

<<<<<<< HEAD
from .forms import StartupForm
from .models import Search
=======
from .forms import StartupForm, SimpleStartupForm
from .models import Startup
>>>>>>> 6fe9bec7cc0be2c0ae2e54ef251c840ddd63e469

def main(request):
    return render(request, 'main.html')

def startup_index(request):
    context = {
        'watching': Startup.objects.all()[:3],
        'trending': Startup.objects.all(),
        'technology': Startup.objects.all(),# filter(category=24),
    }
    return render(request, 'startups/index.html', context)

def startup_search_results(request):
    return JsonResponse(list(Search.objects.all().values()), safe=False)


def startup_show(request, id):
<<<<<<< HEAD
    context = { 'startup': list(filter(lambda s: s['id'] == id, data)) }
    print(context)
=======
    context = { 'startup': Startup.objects.filter(id = id).first() }
>>>>>>> 6fe9bec7cc0be2c0ae2e54ef251c840ddd63e469
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
<<<<<<< HEAD
            r#eturn redirect('project_detail', id=startup.id)
=======
            return redirect('startup_show', id=startup.id)
>>>>>>> 6fe9bec7cc0be2c0ae2e54ef251c840ddd63e469
    else:
        form = StartupForm()
    return render(request, 'startups/new.html', {'form': form })

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

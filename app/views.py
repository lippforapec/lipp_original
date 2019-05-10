from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic

from .forms import StartupForm
from .models import Search

data = [{'id': 1, 'name': 'startup1'}, {'id':2, 'name': 'startup2'}]

def startup_index(request):
    context = {
        'startups': data
    }
    return render(request, 'startups/index.html', context)

def startup_search_results(request):
    return JsonResponse(list(Search.objects.all().values()), safe=False)


def startup_show(request, id):
    context = { 'startup': list(filter(lambda s: s['id'] == id, data)) }
    print(context)
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
            r#eturn redirect('project_detail', id=startup.id)
    else:
        form = StartupForm()
    return render(request, 'startups/new.html', {'form': form})

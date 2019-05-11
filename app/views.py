from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.forms.models import model_to_dict
from django.db.models import Max,F


from .forms import StartupForm, SimpleStartupForm, CustomUserCreationForm
from .models import Startup, Search, Like, Feedback

# for accounts
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required

def main(request):
    return render(request, 'main.html')

@login_required
def startup_index(request):
    context = {
        'watching': Startup.objects.all()[:3],
        'trending': Startup.objects.all(),
        'technology': Startup.objects.all(),# filter(category=24),
    }
    return render(request, 'startups/index.html', context)

@login_required
def startup_show(request, id):
    startup_obj = Startup.objects.filter(id = id).first()
    like = Like.objects.filter(startup = startup_obj,liked=True).all()
    liked = False # did request user like?
    is_owner = False # request user is the owner of this startup?
    like = Like.objects.filter(startup = startup_obj)\
            .order_by('user', '-created_at').distinct('user')
    
    if request.user == startup_obj.user:
        is_owner = True
    # 이건 이거로 하면 안되게따... jquery 처리 필요
    liked = like.filter(user=request.user).first().liked
    like_count = like.filter(liked=True).count()
    search = Search.objects.filter(category = startup_obj.category).first()
    article = search.results[:2]
    print(Feedback.objects.filter(startup=startup_obj).all().values())
    #print(startup_obj.startup_feedbacks)
    context = { 'startup':  startup_obj,
                'article': article ,
                'is_owner':is_owner,
                'liked': liked,
                'likes' : like_count,
                'feedbacks' : Feedback.objects.filter(startup=startup_obj).all()
              }
    return render(request, 'startups/show.html', context)

# form: https://tutorial.djangogirls.org/ko/django_forms/
@login_required
def startup_new(request):
    if request.method == "POST":
        form = StartupForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
            #startup.user = request.user
            #startup.created_at = timezone.now()
            #startup.save()
            return redirect('startup_show', id=startup.id)
    else:
        form = StartupForm()
    return render(request, 'startups/new.html', {'form': form })

@login_required
def startup_edit(request, id):
    startup = Startup.objects.get(id = id)
    if request.user == startup.user:
        sd = model_to_dict(startup)
        if request.method == "POST":
            form = SimpleStartupForm(request.POST, instance = startup)
            if form.is_valid():
                startup = form.save(commit=False)
                startup.user = request.user 
                startup.save()
                return redirect('startup_show', id = startup.id)
            else:
                print(form.errors)
                return render(request, 'startups/edit.html', {'form': StartupForm(initial=sd), 'id': startup.id, 'errors': form.errors})
        else:
            sd['tags'] = str(sd['tags']).replace("[","").replace("\"","").replace("]","")
        return render(request, 'startups/edit.html', {'form': StartupForm(initial=sd), 'id': startup.id})
    else:
        response = HttpResponse("<h2>Page Not Found<h2>")
        response.status_code = 404
        return response






def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        f = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': f})
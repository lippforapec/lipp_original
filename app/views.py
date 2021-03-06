from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.forms.models import model_to_dict
from django.db.models import Count


from .forms import StartupForm, CustomUserCreationForm, LikeForm, FeedbackForm, UsertypeForm
from .models import Startup, Search, Like, Feedback, Usertype
import app.categories as cate

# for accounts
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


# like
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def main(request):
    return render(request, 'main.html')

@login_required
def startup_index(request):
    print(Startup.objects.filter(startup_likes__user = request.user).all())
    context = {
        'watching': Startup.objects.filter(startup_likes__user = request.user).all(),
        'trending': Startup.objects.all().values().annotate(total=Count('startup_likes')).order_by('-total')[:6],
        'financial': Startup.objects.filter(category=18),
        'travel': Startup.objects.filter(category=45),
        'commerce': Startup.objects.filter(category=7),
    }
    return render(request, 'startups/index.html', context)

@login_required
def startup_show(request, id):
    startup_obj = Startup.objects.filter(id = id).first()
    is_owner = request.user == startup_obj.user # request user is the owner of this startup?
    # like data
    # first 는 나중에 지우기
    likes = startup_obj.startup_likes.all()
    request_user_like = likes.filter(user=request.user).first()
    like_count = likes.count()
    # article data
    search = Search.objects.filter(category = startup_obj.category).first()
    article = None
    if search != None:
        article = search.results[:6]
    print(Feedback.objects.filter(startup=startup_obj).all())
    context = { 'startup': startup_obj,
                'article': article ,
                'is_owner': is_owner,
                'cover_photo_url': getattr(startup_obj.cover_photo, 'url', None),
                'request_user_like': request_user_like,
                'likes' : like_count,
                'feedbacks' : Feedback.objects.filter(startup=startup_obj).all().order_by('-created_at')
              }
    return render(request, 'startups/show.html', context)

# form: https://tutorial.djangogirls.org/ko/django_forms/
@login_required
def startup_new(request):
    if request.method == "POST":
        print(request.method)
        form = StartupForm(request.POST, request.FILES)
        if form.is_valid():
            startup=form.save(commit = False)
            startup.user = request.user
            startup.save()
            return redirect('startup_show', id=startup.id)
        return render(request, 'startups/new.html', {'form': form })
    elif request.method == "GET":
        if hasattr(request.user, 'startup') != False:
            return redirect('startup_edit', id=request.user.startup.id)
        else:
            form = StartupForm()
            return render(request, 'startups/new.html', {'form': form })

@login_required
def startup_edit(request, id):
    startup = Startup.objects.get(id = id)
    if request.user == startup.user:
        sd = model_to_dict(startup)
        print(sd)
        if request.method == "POST":
            form = StartupForm(request.POST, request.FILES, instance = startup)
            if form.is_valid():
                startup = form.save(commit=False)
                startup.user = request.user
                startup.save()
                return redirect('startup_show', id = startup.id)
            else:
                return render(request, 'startups/edit.html', {'form': StartupForm(initial=sd), 'id': startup.id, 'errors': form.errors})
        else:
            sd['tags'] = str(sd['tags']).replace("[","").replace("\"","").replace("]","")
        return render(request, 'startups/edit.html', {'form': StartupForm(initial=sd), 'id': startup.id})
    else:
        response = HttpResponse("<h2>Page Not Found<h2>")
        response.status_code = 404
        return response

def like_delete(request,startup_id):
    query = Like.objects.filter(user=request.user, startup_id=startup_id)
    query.delete()

    response = HttpResponse(Like.objects.filter(startup_id=startup_id).all().count())
    response.status_code = 200
    return response

def like_create(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid() and len(Like.objects.filter(startup_id=form.cleaned_data['startup_id'], user=request.user)) == 0:
            like = form.save(commit=False)
            like.user = request.user
            like.save()
    response = HttpResponse(like.startup.startup_likes.all().count())
    response.status_code = 200
    return response

# feedbacks
@login_required
def feedback_create(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        print(form.data)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return HttpResponse(status=200)
        response = HttpResponse("<h2>Page Not Found<h2>")
        response.status_code = 404
        return response

# Signup view for users
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            # automatic login
            login(request, new_user)
            return redirect("usertype")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def get_user_type(request):
    if request.method == 'POST':
        form = UsertypeForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            data = request.POST.copy()
            usertype = data.get('type')
            f.user = request.user
            f.save()
            if usertype == '0':
                return redirect('startup_new')
            else:
                return redirect("startup_index")
    elif request.method == "GET":
        form = UsertypeForm()
        return render(request, 'registration/usertype.html', {'form': form})

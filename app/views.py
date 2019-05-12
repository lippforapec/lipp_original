from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.forms.models import model_to_dict
from django.db.models import Max,F


from .forms import StartupForm, SimpleStartupForm, CustomUserCreationForm, LikeForm
from .models import Startup, Search, Like, Feedback

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
    context = {
        'watching': Startup.objects.all()[:3],
        'trending': Startup.objects.all(),
        'technology': Startup.objects.all(),# filter(category=24),
    }
    return render(request, 'startups/index.html', context)

@login_required
def startup_show(request, id):
    startup_obj = Startup.objects.filter(id = id).first()
    like = startup_obj.startup_likes.all()
    liked = False # did request user like?
    is_owner = False # request user is the owner of this startup?    
    if request.user == startup_obj.user:
        is_owner = True
    print(startup_obj)
    # like data
    # first 는 나중에 지우기
    print("this is problem")
    request_user_like = like.filter(user=request.user).first()
    print(request_user_like)
    like_count = like.count()
    print(like_count)
    # article data
    search = Search.objects.filter(category = startup_obj.category).first()
    article = search.results[:2]
    #print(Feedback.objects.filter(startup=startup_obj).all().values())
    #print(startup_obj.startup_feedbacks)
    #request_user_like
    print(Feedback.objects.filter(startup=startup_obj).all())
    context = { 'startup':  startup_obj,
                'article': article ,
                'is_owner':is_owner,
                'request_user_like': request_user_like,
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

# create and delete user in like 
#class CreateLike(LoginRequiredMixin, generic.CreateView):
#    model = Like 
#    def form_valid(self, form):
#        print("jey")
        #form.instance.user = self.request.user
        #super(CreateHall, self).form_valid(form)
#        return 
    
    
#class DeleteLike(generic.DeleteView):
#    model = Like

def like_delete(request,startup_id):
    query = Like.objects.filter(user=request.user,startup_id=startup_id)
    query.delete()
    return HttpResponse("Deleted!")


def like_create(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        #print(request.cleaned_data)
        if form.is_valid():
            print("its's safe")
            like = form.save(commit=False)
            like.user = request.user
            like.save()
            return HttpResponse('')
        print("no..")
        return HttpResponse('')

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
            return redirect("startup_index")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
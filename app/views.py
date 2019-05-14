from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.forms.models import model_to_dict


from .forms import StartupForm, CustomUserCreationForm, LikeForm, FeedbackForm
from .models import Startup, Search, Like, Feedback
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
    context = {
        'watching': Startup.objects.all()[:3],
        'trending': Startup.objects.all(),
        'technology': Startup.objects.all(),# filter(category=24),
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
        article = search.results[:2]
    print(Feedback.objects.filter(startup=startup_obj).all())
    context = { 'startup': startup_obj,
                'article': article ,
                'is_owner': is_owner,
                # 'cover_photo_url': getattr(startup_obj.cover_photo, 'url', None),
                'request_user_like': request_user_like,
                'likes' : like_count,
                'feedbacks' : Feedback.objects.filter(startup=startup_obj).all()
              }
    return render(request, 'startups/show.html', context)

# form: https://tutorial.djangogirls.org/ko/django_forms/
# form field 별로 다르게 field 받고 ,form 받은 것을 하나하나 확인해가면서 추가하기
@login_required
def startup_new(request):
    if request.method == "POST":
        print(request.method)
        # post 가 필요한 모든 필드가 안들어와서 valid 하지 않은 상태
        form = StartupForm(request.POST)
        #data = request.POST.copy()
        #print(data.get('product_name'))
        #print(data.get('product_name'))
        if form.is_valid():
            startup=form.save(commit = False)
            startup.user = request.user
            startup.save()
            return redirect('startup_show', id=startup.id)
        return render(request, 'startups/new.html', {'form': form })
    elif request.method == "GET":
        if hasattr(request.user, 'startup') != None:
            return redirect('startup_edit', id=request.user.startup.id)
        else:
            form = StartupForm()
            return render(request, 'startups/new.html', {'form': form })

@login_required
def startup_edit(request, id):
    startup = Startup.objects.get(id = id)
    if request.user == startup.user:
        sd = model_to_dict(startup)
        if request.method == "POST":
            form = StartupForm(request.POST, instance = startup)
            if form.is_valid():
                startup = form.save(commit=True)
                # return redirect('startup_show', id = startup.id)
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
    query = Like.objects.filter(user=request.user, startup_id=startup_id)
    query.delete()

    response = HttpResponse(Like.objects.filter(startup_id=startup_id).all().count())
    response.status_code = 200
    return response

def like_create(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        #print(request.cleaned_data)
        if form.is_valid():
            print("its's safe")
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
            print("its's safe")
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return HttpResponse('success!')
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
            return redirect("startup_index")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login_page/') #redirect when user is not logged in
def receipes(request):
    if request.method == "POST":
    
        data = request.POST
        # print(data)
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        print(receipe_name)
        print(receipe_description)
        print(receipe_image)

        Recipe.objects.create(
            receipe_name = receipe_name,
            receipe_description = receipe_description,
            receipe_image = receipe_image
            )

        return redirect ('/receipes/')
        
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
                                   
    context ={'receipes' : queryset}
    return render(request, "receipes.html",context )
    # return HttpResponse("Hii")



def delete_recipe(request, id):
    queryset = Recipe.objects.get(id =id)
    queryset.delete()
    # print(id)
    # return HttpResponse("a")
    return redirect ('/receipes/')

def update_recipe(request,id):
    queryset = Recipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST

        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image

        # receipe_name = receipe_name
        # receipe_description = receipe_description
        # receipe_image = receipe_image

        Recipe.objects.create(
            receipe_name = queryset.receipe_name,
            receipe_description = queryset.receipe_description,
            receipe_image = queryset.receipe_image,
        )
        
        queryset.save()

        return redirect ('/receipes/')

    context = {'receipe' : queryset}
    return render(request,"update_recipe.html",context)


def user_signup(request):
    if request.method == "POST":
        # data =request.POST 

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username =request.POST.get('username')
        password = request.POST.get('password')

        print(first_name)
        print(last_name)
        print(username)

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request,'Username already taken')
            return redirect('/user_signup/')
       

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()
        val = User.objects.all()
        print(val)
        
        messages.info(request,'Your account created successfully')

        return redirect('/user_signup/')

    return render(request, "register.html")
    

def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # user = User.objects.all()

        # if not User.objects.filter (username = username).exists():
        #     messages.error(request, 'Invalid Username')
        #     return redirect('/login_page/')
            
        users = authenticate(username = username, password = password)
        if users is None:
            messages.error(request, 'Invalid password')
            return redirect('/login_page/')
        
        else:
            login(request,users)
            return redirect('/receipes/')

    return render(request, "login.html")

def log_out(request):
    logout(request)
    return redirect('/login_page/')


    



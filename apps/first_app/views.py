from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import error
from .models import *
import bcrypt

def index(request):
    return render(request, "first_app/index.html")

def register(request):
    errors = User.objects.regvalidator(request.POST)

    if len(errors):
        for error in errors.itervalues():
            messages.error(request, error)
        return redirect("/")

    else:
        new_user = User.objects.create(first_name=request.POST["first_name"], alias=request.POST["alias"], email=request.POST["email"], password=bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()), birthday = request.POST["bday"])
        request.session["id"] = new_user.id
        # messages.success(request, "Successfully registered!")
        return redirect("/friends")

def login(request):
    result = User.objects.logvalidator(request.POST)
    print result
    print type(result)

    if result == 'Invalid email or password.':
        messages.error(request, result)
        return redirect("/")
    
    request.session["id"] = result.id
    # messages.success(request, "Successfully loggedin!")
    return redirect("/friends")

def logout(request):
    del request.session["id"]
    return redirect ("/")

def show_friends(request):
    myself = User.objects.get(id=request.session["id"])
    
    try:
        notmes = User.objects.exclude(id = request.session["id"])
        print "+++++NOT_ME+++++"

    except:
        users = None

    try:
        myfriendships = Friend.objects.filter(user = myself)

        myfriends = []
        for myfriendship in myfriendships:
            myfriends.append(myfriendship.user2)
        
        notfriends = []
        for notme in notmes:
            if (notme not in myfriends):
                notfriends.append(notme)

    except:
         myfriendships = None

    context = {
            "myself": myself,
            "myfriends": myfriends,
            "notfriends": notfriends,
        }
    return render(request, "first_app/showfriends.html", context)

def add_friend(request, id):
    user = User.objects.get(id=request.session["id"])
    friend = User.objects.get(id = id)

    Friend.objects.create(user = user, user2 = friend)
    Friend.objects.create(user = friend, user2 = user)

    return redirect ("/friends")

def remove_friend(request, id):
    user = User.objects.get(id=request.session["id"])
    friend = User.objects.get(id = id)

    # for row in Friend.objects.all():
    #     if Friend.objects.filter(user = user, user2 = friend).count() > 1:
    #         row.delete()

    friendship1 = Friend.objects.get(user = user, user2 = friend)
    friendship2 = Friend.objects.get(user = friend, user2 = user)


    friendship1.delete()
    friendship2.delete()

    return redirect ("/friends")

def show_profile(request, id):
    user = User.objects.get(id = id)

    context = {
        'user': user,
    }
    return render(request, "first_app/showprofile.html", context)

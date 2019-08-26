from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'belt_exam_app/index.html')
def register(request):
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pass_to_hash = request.POST['password']
            hashed_pass = bcrypt.hashpw(pass_to_hash.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pass)
            request.session["user_id"] = new_user.id
            return redirect('/')
def login(request):
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        form = request.POST
        try:
            print('trying...')
            user = User.objects.get(email=form["email"])
        except:
            print('no success')
            messages.error(request, "Check your email and password!")
            return redirect("/")
        if bcrypt.checkpw(form['password'].encode(), user.password.encode()):
            print('passwords matched')
            request.session["user_id"] = user.id
            return redirect('/')
            messages.error(request, "Check your email and password!")
        print('no match')
        return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')
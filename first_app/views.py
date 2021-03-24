from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	
	return render(request, "registration.html")

def create_user(request):
	if request.method == 'POST':
		errors = User.objects.basic_validator(request.POST)
		if errors:
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		else:
			hashedpw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
			print(request.POST['password'])
			print(hashedpw)
			create_new = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password= hashedpw)
			request.session['user_id'] = create_new.id
			return redirect('/success') 
	else: 
		redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.login_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		else:
			user = User.objects.get(email=request.POST['login_email'])
			request.session['user_id'] = user.id
			return redirect('/success')
	else:
		redirect('/')

def success(request):
	one_user = User.objects.get(id=request.session['user_id'])
	context = {
		"one_user": one_user
	}
	return render(request,'success.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')
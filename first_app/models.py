from django.db import models
import re
from .models import *
import bcrypt

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		
		if len(postData['first_name']) < 2:
			errors['first_name'] = "First name should be at least 2 characters."
		else: 
			FIRSTNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
			if not FIRSTNAME_REGEX.match(postData['first_name']):
				errors['first_name'] = "First name must contain only letters."
		if len(postData['last_name']) < 2:
			errors['last_name'] = "Last name should be at least 2 characters."
		else:
			LASTNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
			if not LASTNAME_REGEX.match(postData['last_name']):
				errors['last_name'] = "Last name must contain only letters."	
		if len(postData['email']) == 0:
			errors['email']	= "Email address required."
		else:
			EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
			if not EMAIL_REGEX.match(postData['email']):
				errors['email'] = "Invalid email address!"
		email = self.filter(email=postData['email'])
		if email:
			errors['email'] = "Email address already used."		
		if len(postData['password']) < 8:
			errors['password']	= "Password must be at least 8 characters."
		if postData['password'] != postData['confirmPassword']:
			errors['password'] = 'Passwords must match'
		return errors

	def login_validator(self, postData):
		errors = {}
		login_email = User.objects.filter(email=postData['login_email'])
		if len(login_email) > 0:
			if bcrypt.checkpw(postData['login_pass'].encode(),login_email[0].password.encode()):
				print("password matches")
			else:
				errors['login_email'] ='Password does not match'
		else:
			errors['login_email'] = 'User with that email does not exist'
		return errors 		

class User(models.Model):
	first_name= models.CharField(max_length=45)
	last_name= models.CharField(max_length=45)
	email= models.CharField(max_length=60)
	password=models.CharField(max_length=80)
	created_at= models.DateTimeField(auto_now_add = True)
	updated_at=models.DateTimeField(auto_now_add = True)
	objects = UserManager()



from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r"^[a-zA-Z\s]+$")

class UserManager(models.Manager):
    def regvalidator(self, postData):
        errors = {}
        if len(postData["first_name"]) < 1:
            errors["first_name"] = "First name is required."
        elif len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must contain at least two characters."
        elif not NAME_REGEX.match(postData["first_name"]):
            errors["first_name"] = "First name contains invalid characters."

        if len(postData["alias"]) < 1:
            errors["alias"] = "Alias is required."
        elif len(postData["alias"]) < 2:
            errors["alias"] = "Alias must contain at least two characters."
        elif not NAME_REGEX.match(postData["alias"]):
            errors["alias"] = "Alias contains invalid characters."

        if len(postData["bday"]) < 1:
            errors["email"] = "Birthday is required."

        if len(postData["email"]) < 1:
            errors["email"] = "Email is required."
        elif not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address."

        if len(postData["pw"]) < 8:
            errors["pw"] = "Password must contain at least 8 characters."
        elif not postData["pw"] == postData["pw_confirm"]:
            errors["pw"] = "Password and confirmation do not match."

        if not errors and User.objects.filter(email=postData["email"]):
            errors["email"] = "Email address is already in use."

        return errors

    def logvalidator(self, postData):
        try:
            user_to_login = User.objects.get(email = postData["email"])
            print "USER TO LOGIN", user_to_login
            print user_to_login.password
            if bcrypt.checkpw(postData['pw'].encode(), user_to_login.password.encode()):
                print "USER TO LOGIN2", user_to_login
                return user_to_login
        except:
            pass
        return "Invalid email or password."

class User(models.Model):
    first_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.email

class Friend(models.Model):
    user = models.ForeignKey(User, related_name = "adding_user")
    user2 = models.ForeignKey(User, related_name = "accepting_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
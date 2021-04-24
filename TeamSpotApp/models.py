from django.db import models
import re
from datetime import datetime, timedelta
from django.utils import timezone


#*********************LOGIN AND REGISTRATION***********************
class UserManager(models.Manager):
  def register_validator(self, postData):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if not EMAIL_REGEX.match(postData['email']) and len(postData['email']) != 0:
      errors['email'] = "Invalid email address format"

    if len(postData['first_name']) < 2 and len(postData['first_name']) != 0:
      errors['first_name_short'] = "First name must be at least 2 characters"

    if len(postData['last_name']) < 2 and len(postData['last_name']) != 0:
      errors['last_name_short'] = "Last name must be at least 2 characters"
      
    if len(postData['password']) < 8 and len(postData['password']) != 0:
      errors['password_short'] = "Password must be at least 8 characters"

    if postData['password'] != postData['conf_password']:
      errors['match'] = "Passwords do not match"

    for user in User.objects.all():
      if user.email == postData['email']:
        errors['email_exists'] = "An account with this email address exists already."

    if len(postData['first_name']) ==0 or len(postData['last_name']) ==0 or len(postData['email']) ==0 or len(postData['password']) == 0 or len(postData['conf_password']) == 0:
      errors['empty_fields'] = "Please fill out all Registration fields."

    return errors

  def login_validator(self, postData):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if not EMAIL_REGEX.match(postData['email']) and len(postData['email']) != 0:
      errors['login_email'] = "Invalid email address format"

    if len(postData['email']) == 0 or len(postData['password']) == 0 :
      errors['login_email_password_empty'] = "Please enter both an email and a password."

    return errors
#************************END LOGIN AND REGISTRATION*******************


class User(models.Model):
  first_name = models.TextField()
  last_name = models.TextField()
  email = models.TextField()
  password = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = UserManager()

class MessageManager(models.Manager):
  def message_validator(self, postData):
    errors = {}
    if len(postData['message']) < 1:
      errors['message_blank'] = "Cannot post blank message"
    return errors

class Message(models.Model):
  poster = models.ForeignKey(User, related_name = "user_message", on_delete = models.CASCADE, null=True)
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = MessageManager()


class CommentManager(models.Manager):
  def comment_validator(self, postData):
    errors = {}
    if len(postData['comment']) < 1:
      errors['comment_blank'] = "Cannot post blank comment"
    return errors 


class Comment(models.Model):
  poster = models.ForeignKey(User, related_name = "user_comment", on_delete = models.CASCADE, null=True)
  post = models.ForeignKey(Message, related_name = "message_comment", on_delete = models.CASCADE, null=True)
  comment = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = CommentManager()

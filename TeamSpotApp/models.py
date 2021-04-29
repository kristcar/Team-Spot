from django.db import models
import re
from datetime import datetime, timedelta
from django.utils import timezone
from django import forms

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



#************************** MESSAGE BOARD *********************************#

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

#************************** END MESSAGE BOARD *********************************#

#**************************** PROJECTS ***************************************#

class ProjectManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        #validate length of project name
        if len(postData['name']) < 5:
            errors['name'] = "A project's name must be at least five characters long."
        #validate length of project description
        if len(postData['desc']) < 10:
            errors['desc'] = "A project's description must be at least ten characters long."
        #make sure project name is unique to avoid confusion
        current_projects = Project.objects.filter(project_name = postData['name'])
        if len(current_projects) > 0:
            errors['duplicate'] = "That project name is already in use."
        return errors

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name="projects_created", on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="projects_joined")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ProjectManager()

#***************************** END PROJECTS **********************************#


#**************************** ACTION ITEM ***************************************#
class TaskManager(models.Manager):
  def task_validator(self, postData):
    errors = {}
    if len(postData['title']) < 4 or len(postData['description']) < 4:
      errors['task_description_short'] = "Task title or description is too short"
    if postData["due_date"] < datetime.now().strftime("%m-%d-%Y"):
      errors["due_date_past"] = "Please select a due date in the future"
    return errors


class Task(models.Model):
  creator = models.ForeignKey(User, related_name = "user_task", on_delete = models.CASCADE)
  title = models.CharField(max_length = 250)
  due_date = models.DateTimeField()
  description = models.CharField(max_length = 1000)
  response = models.CharField(max_length = 1000, default = "", blank = True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)
  assigned_to = models.ForeignKey(User, related_name = "assigned_task", on_delete = models.CASCADE, blank = True, null = True)
  project = models.ForeignKey(Project, related_name = "project_task", on_delete = models.CASCADE, blank =True, null = True)
  objects = TaskManager()
#***************************** END ACTION ITEM **********************************#

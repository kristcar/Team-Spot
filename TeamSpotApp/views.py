from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Count

#************************LOGIN AND REGISTRATION********************

def loginRegister(request):
  return render(request, 'loginReg.html')


def register(request):
  if request.method == "POST":
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0: 
      for key, value in errors.items():
        messages.error(request, value)
      return redirect("/")
    else: 
      hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
      print(hashed_pw)
      user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password=hashed_pw)
      request.session['user_id'] = user.id
      return redirect('/dashboard')
  else:
    return redirect('/')
    

def login(request):
  if request.method == 'POST':
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0: 
      for key, value in errors.items():
        messages.error(request, value)
      return redirect("/")
    user = User.objects.filter(email=request.POST['email']) 
    if len(user) > 0:
      user = user[0]
      if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        return redirect('/dashboard')
  messages.error(request, "Email or password is incorrect")
  return redirect('/')


def logout(request):
  request.session.clear()
  return redirect('/')

#********************END LOGIN AND REGISTRATION*********************

def catch_all(request, url):
  return redirect('/')


def dashboard(request):
  if "user_id" not in request.session: 
    messages.error(request, "Please log in or register")
    return redirect('/')
  context = {
    "current_user": User.objects.get(id = request.session['user_id']),
  }
  return render(request, 'dashboard.html', context)


#********************MESSAGE BOARD*********************
def chat(request):
  if "user_id" in request.session: 
    context = {
      "all_messages": Message.objects.all(),
      "current_user": User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'chat.html', context)
  else:
    messages.error(request, "Please log in or register")
    return redirect('/')


def post_message(request):
  if request.method == "POST":
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
    else: 
      message = Message.objects.create(message = request.POST['message'], poster = User.objects.get(id = request.session['user_id']))
  return redirect('/chat')

def post_comment(request, message_ID):
  if request.method == "POST":
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
    else:
      comment = Comment.objects.create(
        comment = request.POST['comment'], 
        poster = User.objects.get(id = request.session['user_id']),        
        post = Message.objects.get(id = message_ID) 
        )
  return redirect('/chat')

def delete(request, message_ID):
  if request.method == "POST":
    message_to_delete = Message.objects.get(id = message_ID)
    message_to_delete.delete()
  return redirect('/chat')

def delete_comment(request, comment_ID):

  comment_to_delete = Comment.objects.get(id = comment_ID)
  comment_to_delete.delete()
  return redirect('/chat')


#********************END MESSAGE BOARD*********************

#******************** OPEN ACTION ITEMS ********************

def open_items(request):
  if "user_id" in request.session: 
    context = {
      "all_tasks": Task.objects.all(),
      "current_user": User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'openItems.html', context)
  else:
    messages.error(request, "Please log in or register")
    return redirect('/')

def item_page(request, task_ID):
  if "user_id" in request.session: 
    context = {
      "all_tasks": Task.objects.all(),
      "one_task": Task.objects.get(id = task_ID),
      "current_user": User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'item.html', context)
  else:
    messages.error(request, "Please log in or register")
    return redirect('/')

def add_new_item(request):
  if "user_id" in request.session: 
    context = {
      "current_user": User.objects.get(id = request.session['user_id']),
      "all_users": User.objects.all()
    }
    return render(request, 'add_new_item.html', context)
  else:
    messages.error(request, "Please log in or register")
    return redirect('/')  

def create_action_item(request, user_ID):
  if request.method == "POST":
    errors = Task.objects.task_validator(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/open_items/add_new_item')
    else:
      task = Task.objects.create(
        creator = User.objects.get(id = request.session['user_id']),   
        title = request.POST['title'],      
        description = request.POST['description'],
        due_date = request.POST['due_date'],
        assigned_to = User.objects.get(id = request.POST['assigned_to']))
      return redirect('/open_items')

def delete_action_item(request, task_ID):
  if "user_id" not in request.session: 
    messages.error(request, "Please log in or register")
    return redirect('/')
  tasks_with_id = Task.objects.filter(id = task_ID)
  if len(tasks_with_id) == 0: #not in database
    return redirect('/open_items')
  if request.method == "POST":
    task_to_delete=Task.objects.get(id=task_ID)
    #Verify owner is the person logged in in session for delete permissions:
    if task_to_delete.creator.id == request.session['user_id']:
      task_to_delete.delete()
  return redirect('/open_items')

def post_response(request, task_ID):
  if "user_id" not in request.session: 
    messages.error(request, "Please log in or register")
    return redirect('/')
  if request.method == "POST":
    task_to_update=Task.objects.get(id=task_ID)
    task_to_update.response = request.POST['response']
    task_to_update.save()
  return redirect(f'/open_items/item_page/{task_ID}')



#******************* END ACTION ITEMS  **********************
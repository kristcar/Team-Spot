from django.urls import path  
from . import views  

urlpatterns = [
  path('', views.loginRegister),
  path('register', views.register),
  path('login', views.login),
  path('logout', views.logout),
  path('dashboard', views.dashboard),

  path('chat', views.chat),
  path('chat/postMessage', views.post_message),
  path('chat/postComment/<int:message_ID>', views.post_comment),
  path('delete/<int:message_ID>', views.delete),
  path('delete_comment/<int:comment_ID>', views.delete_comment),

  path('open_items', views.open_items),
  path('open_items/item_page/<int:task_ID>', views.item_page),
  path('open_items/add_new_item', views.add_new_item),
  path('/create_action_item', views.create_action_item),

  path('<url>', views.catch_all),
]
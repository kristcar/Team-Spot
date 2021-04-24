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

  path('<url>', views.catch_all),
]
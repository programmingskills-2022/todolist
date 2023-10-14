from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name='home'),
    path('add/', views.addTodo , name='add'),
    path('delete/<str:pk>/',views.deleteTodo, name='delete-todo'),
    path('edit/<str:pk>/',views.editTodo, name='edit-todo'),
    path('/<str:pk>/', views.showTodo, name='todo-show'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register')
    
]
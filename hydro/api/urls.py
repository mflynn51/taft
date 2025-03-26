from django.urls import path

from . import views

urlpatterns = [
    path('points/', views.GeoList.as_view()),
    path('points/', views.GeoListCreate.as_view()),
    #path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    #path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()),
    #path('signup/', views.signup),
    #path('login/', views.login),

]


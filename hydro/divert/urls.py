from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("<int:location_id>", views.location_point, name="location_point"),
    path('delete-all-pods/', views.delete_all_pods, name='delete_all_pods'),
    path('location/', views.location, name="location"),
    path('map_river/', views.map_river, name='map_river'),
    path('map_aws/', views.map_aws, name='map_aws'),
    path('map_aws_libre/', views.map_aws_libre, name='map_aws_libre'),
    path('map_golf/', views.map_golf, name='map_golf'),
    path('map_putt/', views.map_putt, name='map_putt'),
    #path('map_foo/', views.map_foo, name='map_foo'),
    path('delete_geo_point/<int:location_id>', views.delete_geo_point, name='delete_geo_point'),

    #path('divert/', include("divert.urls")),
    path('api/', include("api.urls")),
    
    
]
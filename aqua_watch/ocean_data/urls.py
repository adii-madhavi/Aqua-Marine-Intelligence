from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'), 
    path('dashboard/', views.home, name='home'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/signup/', views.signup_api, name='signup_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    path('api/add-record/', views.add_record_api, name='add_record_api'),
    path('api/get-all-records/', views.get_all_records, name='get_all_records'),
    path('api/species/', views.species_api, name='species_api'),
    path('api/recommend/', views.recommend_species_api, name='recommend_species'),
    path('api/search-water-body/', views.search_water_body, name='search_water_body'),
]
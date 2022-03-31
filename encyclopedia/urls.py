from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('searchResults', views.displaySearchResults ,name='searchResults'),
    path('new', views.createEntry, name='newEntry'),
    path('rand', views.randomPage, name='randomPage'),
    path('edit/<str:name>', views.editPage, name='editPage'),
    path('<str:name>', views.displayEntry, name='entryName')
]

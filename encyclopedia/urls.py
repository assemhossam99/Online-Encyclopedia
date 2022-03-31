from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('searchResults', views.displaySearchResults ,name='searchResults'),
    path('new', views.createEntry, name='newEntry'),
    path('edit/<str:name>', views.editPage, name='editPage'),
    path('<str:name>', views.displayEntry, name='entryName')
]

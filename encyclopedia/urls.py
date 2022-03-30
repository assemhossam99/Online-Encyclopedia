from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('searchResults', views.displaySearchResults ,name='searchResults'),
    path('<str:name>', views.displayEntry, name='entryName')
]

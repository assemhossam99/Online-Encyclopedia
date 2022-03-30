from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from . import util

class SearchForm(forms.Form):
    search = forms.CharField(widget= forms.TextInput (attrs={'placeholder':'Search Encyclpedia'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : SearchForm()
    })

def displayEntry(request, name):
    entryText = str(util.get_entry(name))
    return render(request, 'encyclopedia/entry.html', {
        'title' : name,
        'entryText' : entryText,
        "form" : SearchForm()
    })

def displaySearchResults(request):
    Entries = util.list_entries()
    SearchResultsEntries = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searchText = form.cleaned_data["search"]
            for entry in Entries:
                if searchText.lower() == entry.lower():
                    entryText = str(util.get_entry(searchText.lower()))
                    return render(request, 'encyclopedia/entry.html', {
                        'title' : searchText.lower(),
                        'entryText' : entryText,
                        'form' : SearchForm()
                     })
                elif searchText.lower() in entry.lower():
                    SearchResultsEntries.append(entry)
        else:
            return render(request, 'encyclopedia/results.html', {
                "form" : form
            })
    return render(request, 'encyclopedia/results.html',{
        'Entries' : SearchResultsEntries,
        "form" : SearchForm()
    })


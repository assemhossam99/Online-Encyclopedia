from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
import random
import markdown2

class newEntryForm(forms.Form):
    entryTitle = forms.CharField(widget= forms.TextInput (attrs={'class' : 'entryTitleField', 'placeholder' : 'Title'}), label='')
    entryText = forms.CharField(label='', widget=forms.Textarea(attrs={'class' : 'inputField', 'placeholder' : 'Page Content'}) )

class SearchForm(forms.Form):
    search = forms.CharField(widget= forms.TextInput (attrs={'placeholder':'Search Encyclpedia'}))

class editForm(forms.Form):
    entryText = forms.CharField(widget=forms.Textarea(attrs={'class' : 'inputField', 'plaveholder' : 'Page Content'}), label='')

def convertMarkdown(text):
    retText = markdown2.markdown(text)
    return retText

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : SearchForm()
    })

def displayEntry(request, name):
    entryText = str(util.get_entry(name))
    return render(request, 'encyclopedia/entry.html', {
        'title' : name,
        'entryText' : convertMarkdown(entryText),
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

def createEntry(request):
    entryTitle = ''
    if request.method == 'POST':
        form = newEntryForm(request.POST)
        if form.is_valid():
            entryTitle = form.cleaned_data['entryTitle']
            entryText = form.cleaned_data['entryText']
            allEntries = util.list_entries()
            for i in range(0, len(allEntries)):
                allEntries[i] = allEntries[i].lower()
            if entryTitle.lower() in allEntries:
                return render(request, 'encyclopedia/create.html', {
                    'form' : SearchForm(),
                    'entryForm' : form,
                    'message' : 'Error: there is entry saved with this title.',
                    'error' : 1,
                    'entryTitle' : entryTitle
                })
            else:
                util.save_entry(entryTitle, entryText)
                return HttpResponseRedirect(reverse('entryName', args=[entryTitle]))
        else:
            return render(request, 'encyclopedia/index.html', {
                'form' : form,
                'entryTitle' : entryTitle
            })
    return render(request, 'encyclopedia/create.html', {
        'form' : SearchForm(),
        'entryForm' : newEntryForm(),
        'entryTitle' : entryTitle
    })

def editPage(request, name):
    content = util.get_entry(name)
    content = "".join([s for s in content.strip().splitlines(True) if s.strip()])
    dic = {'entryText' : content}
    if request.method == 'POST':
        form = editForm(request.POST)
        if form.is_valid():
            newContent = form.cleaned_data['entryText']
            util.save_entry(name, newContent)
            return HttpResponseRedirect(reverse('entryName', args=[name]))
        else:
            return render(request, 'encyclopedia/index.html')
    return render(request, 'encyclopedia/edit.html', {
        'form' : SearchForm(),
        'entryName' : name,
        'editForm' : editForm(dic),
        'content' : content
    })

def randomPage(request):
    allEntries = util.list_entries()
    entriesSize = len(allEntries)
    randomNumber = random.randint(0, entriesSize - 1)
    curName = allEntries[randomNumber]
    return HttpResponseRedirect(reverse('entryName', args=[curName]))
    return render(request, 'encyclopedia/layout.html', {
        'toEntry' : curName
    })
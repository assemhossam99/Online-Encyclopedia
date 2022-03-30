from django.shortcuts import render
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def displayEntry(request, name):
    entryText = str(util.get_entry(name))
    # return HttpResponse(entryText)
    return render(request, 'encyclopedia/entry.html', {
        'title' : name,
        'entryText' : entryText
    })


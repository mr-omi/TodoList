from django.shortcuts import render
from .models import ToDoList
from .forms import CreateNew
from django.http import HttpResponseRedirect


def home(response):
    return render(response, "mainapp/home.html", {})


def index(response, id):
    td = ToDoList.objects.get(id=id)
    if response.method == "POST":
        for item in td.item_set.all():
            if response.POST.get("c" + str(item.id)) == "clicked":
                item.complete = True
            else:
                item.complete = False
            item.save()

        if response.POST.get("add"):
            item = response.POST.get("new_item")
            td.item_set.create(name=item, complete=False)

        if response.POST.get("delete"):
            for item in td.item_set.all():
                if item.complete:
                    del_t = item
                    del_t.delete()

    return render(response, "mainapp/index.html", {"td": td})


def create(response):
    if response.method == "POST":
        form = CreateNew(response.POST)
        if form.is_valid():
            nam = form.cleaned_data["name"]
            ls = ToDoList(name=nam)
            ls.save()
            response.user.todolist.add(ls)
            return HttpResponseRedirect("/%i" % ls.id)
    else:
        form = CreateNew()
        return render(response, "mainapp/create.html", {"form": form})


def view(response):
    return render(response, "mainapp/view.html", {})

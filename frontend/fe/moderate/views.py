from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Module, Issue
from .forms import CreateNewMod
from .main import MODeRATE
from collections import Counter
import text2emotion as te


def home(response):
    return render(response, "moderate/home.html", {})

def index(response, code):
    ls = Module.objects.filter(code=code)[0]
    return render(response, "moderate/list.html", {"ls":ls})

def find(response):
    return render(response, "moderate/find.html")

def moderate(request):
    mydict = {}
    emotions_dict = {"Happy": 0.0, "Angry" : 0.0, "Surprise" : 0.0, "Sad" : 0.0, "Fear" : 0.0}
    text = request.POST.get('mod')
    text = text.upper()
    mydict["text"] = text
    try:
        #check if mod is in database
        comments = Module.objects.get(code=text)
        mydict["rating"] = getattr(comments, "rating")
        mydict["comment1"] = getattr(comments, "comment1")
        mydict["comment2"] = getattr(comments, "comment2")
        mydict["comment3"] = getattr(comments, "comment3")
        mydict["emotions"] = list(map(float, getattr(comments, "emotions").split(",")))
        Module.objects.filter(code=text).update(searched=
                                                getattr(comments, "searched") + 1)
    except:
        #perform MODeRATE if not in database
        comments = MODeRATE(text, 2)
        #emotion detection
        for comment in comments[0]:
            emotions_dict = Counter(emotions_dict) + Counter(te.get_emotion(comment))
        mydict["emotions"] = list(emotions_dict.values())
        #rating using AI model
        mydict["rating"] = comments[1]
        #comments
        try:
            mydict["comment1"] = comments[0][0]
        except:
            mydict["comment1"] = ""
        try:
            mydict["comment2"] = comments[0][1]
        except:
            mydict["comment2"] = ""
        try:
            mydict["comment3"] = comments[0][2]
        except:
            mydict["comment3"] = ""
        #save into database
        emo_string = ""
        for e in list(map(str, mydict["emotions"])):
            emo_string += e + ","
        mod = Module(code = text, 
                    rating = comments[1],
                    comment1 = mydict["comment1"],
                    comment2 = mydict["comment2"],
                    comment3 = mydict["comment3"],
                    searched = 1,
                    emotions = emo_string[:-1]
                    )
        mod.save()
    global cmod
    cmod = text
    return render(request, "moderate/comments.html", mydict)

def view(response):
    return render(response, "moderate/view.html")

def rating(response):
    mydict = {}
    top3 = Module.objects.order_by("-rating")[:3]
    mydict["first"] = getattr(top3[0], "code")
    mydict["second"] = getattr(top3[1], "code")
    mydict["third"] = getattr(top3[2], "code")
    mydict["rate1"] = getattr(top3[0], "rating")
    mydict["rate2"] = getattr(top3[1], "rating")
    mydict["rate3"] = getattr(top3[2], "rating")
    return render(response, "moderate/rating.html", mydict)

def searched(response):
    mydict = {}
    top3 = Module.objects.order_by("-searched")[:3]
    mydict["first"] = getattr(top3[0], "code")
    mydict["second"] = getattr(top3[1], "code")
    mydict["third"] = getattr(top3[2], "code")
    mydict["search1"] = getattr(top3[0], "searched")
    mydict["search2"] = getattr(top3[1], "searched")
    mydict["search3"] = getattr(top3[2], "searched")
    return render(response, "moderate/searched.html", mydict)

def problem(request):
    return render(request, "moderate/problem.html")

def thankyou(request):
    text = request.POST.get('problem')
    issue = Issue(code=cmod,message=text)
    issue.save()
    return render(request, "moderate/thankyou.html")
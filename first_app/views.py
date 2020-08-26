from django.shortcuts import render, redirect
from .models import*
from django.contrib import messages
import bcrypt
from django.db.models import Q


def index(request):

    return render(request,'index.htm')

def register(request):
    valErrors=User.objects.reqValidator(request.POST)
    # print(request.POST)
    # print(valErrors)
    if len(valErrors) > 0:
        for key, value in valErrors.items():
            messages.error(request,value)
        return redirect("/")
    else:
        hash1 = bcrypt.hashpw(request.POST['form_pw'].encode(), bcrypt.gensalt()).decode()
        newUser= User.objects.create(firstName=request.POST['form_fname'],lastName=request.POST['form_lname'],email=request.POST['form_email'],password= hash1)
        request.session['loggedInId']=newUser.id
        return redirect('/home')

def login(request):
    validationErrors=User.objects.loginValidator(request.POST)
    if len(validationErrors) > 0:
        for value in validationErrors.values():
            messages.error(request,value)
        return redirect('/')
    else:
        usersWithEmail=User.objects.filter(email=request.POST['form_email'])
        request.session['loggedInId']= usersWithEmail[0].id 
    return redirect('/home')

def home(request):
    if 'loggedInId' not in request.session:
        messages.error(request, "Must Log In First!")
        return redirect('/')
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId'])
    }
    return render(request, 'home.htm', context)


def mainPage(request):
    if 'loggedInId' not in request.session:
        messages.error(request, "Must Log In First!")
        return redirect('/')
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'allQuotes': Quote.objects.all(),
        'likedQuotes' : Quote.objects.filter(likes= User.objects.get(id=request.session['loggedInId'])),
        'notLikedQuotes' : Quote.objects.exclude(likes=User.objects.get(id=request.session['loggedInId'])),
    }
    return render(request, 'mainPage.htm', context)


def createQuote(request):
    validationErrors=Quote.objects.quoteValidator(request.POST)
    if len(validationErrors) > 0:
        for value in validationErrors.values():
            messages.error(request,value)
        return redirect('/Quotes')
    newQuote= Quote.objects.create(content=request.POST['form_quote'], author=request.POST['form_author'], uploader=User.objects.get(id=request.session['loggedInId']))

    return redirect('/Quotes')

def likeQuote(request, quoteId):
    print(quoteId)
    liker = User.objects.get(id=request.session['loggedInId'])
    quote = Quote.objects.get(id=quoteId)
    quote.likes.add(liker)
    return redirect("/Quotes")

def unlike(request, quoteId):
    liker = User.objects.get(id=request.session['loggedInId'])
    quote = Quote.objects.get(id=quoteId)
    quote.likes.remove(liker)
    return redirect("/Quotes")


def userPage(request, userId):
    UserToGet = User.objects.get(id=userId)
    context = {
        'user': UserToGet
    }
    return render(request,'userPage.htm', context)



def deleteQuote(request, quoteId):
    quoteDelete = Quote.objects.get(id=quoteId)
    quoteDelete.delete()
    return redirect('/Quotes')

def edit(request, quoteId ):
    context ={
    'quoteToEdit': Quote.objects.get(id=quoteId)
    }

    return render(request, 'edit.htm', context)

def update(request, quoteId):
    validationErrors=Quote.objects.quoteValidator(request.POST)
    if len(validationErrors) > 0:
        for value in validationErrors.values():
            messages.error(request,value)
        return redirect(f'/edit/{quoteId}')
    quoteToUpdate= Quote.objects.get(id=quoteId)
    quoteToUpdate.author = request.POST['form_author']
    quoteToUpdate.content = request.POST['form_quote']
    quoteToUpdate.save()

    return redirect('/Quotes')



def logout(request):
    request.session.clear()
    return redirect('/')
from django.urls import path
from . import views

urlpatterns= [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('home',views.home),
    path('logout',views.logout),
    path('Quotes',views.mainPage),
    path('createQuote',views.createQuote),
    path('userPage/<int:userId>',views.userPage),
    path('delete/<int:quoteId>',views.deleteQuote),
    path('like/<int:quoteId>',views.likeQuote),
    path('edit/<int:quoteId>',views.edit),
    path('updateQuote/<int:quoteId>',views.update),
    path('unlike/<int:quoteId>', views.unlike),
]
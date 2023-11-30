from django.urls import path
from . import views
urlpatterns=[
    path("", views.add,name = "cal"),
    path("check", views.checkpeople,name = "check"),
    path("food", views.lookup,name = "food"),
    path("nutrition", views.checkfood,name = "nutrition"),
    path("signin", views.signin,name = "signin"),
    path("signout", views.signout,name = "signout"),
    path("signup", views.signup,name = "signup"),
]
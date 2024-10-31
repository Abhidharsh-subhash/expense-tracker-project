from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.loginpage, name='loginpage'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('homepage/', views.homepage, name='homepage'),
    path('otpverificationpage/', views.otpverificationpage, name='otpverification'),
    path('signuppage/', views.signuppage, name='signuppage'),
    path('incomepage/', views.incomepage, name='incomepage'),
    path('addingbudgetpage/', views.addingbudgetpage, name='addingbudgetpage'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('confirm_email', views.confirm_email, name='confirm_email'),
    path('setpassword', views.setpassword, name='setpassword'),
    path('addexpensepage', views.addexpensepage, name='addexpensepage'),
    path('profilepage', views.profilepage, name='profilepage')
]

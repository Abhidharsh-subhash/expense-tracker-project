from django.shortcuts import render, redirect
from .models import Users

# Create your views here.


def index(request):
    return render(request, 'index.html')


def homepage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'homepage.html', {"msg": msg})


def otpverificationpage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'otpverificationpage.html', {"msg": msg})


def signuppage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'signup.html', {"msg": msg})


def signup(request):
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if Users.objects.filter(email=email).exists():
            return redirect('/signuppage?msg=email already exists!')
        Users.objects.create(username=username, email=email, password=password)
        return redirect('/loginpage?msg=You are registered successuflly!')
    return redirect('/signuppage?msg=Please signup again!')


def budgetpage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'budgetpage.html', {"msg": msg})


def addingbudgetpage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'addingbudgetpage.html', {"msg": msg})


def loginpage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'loginpage.html', {"msg": msg})


def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Users.objects.get(email=email, password=password)
        except Users.DoesNotExist:
            return redirect('/loginpage?msg=Invalid Email or Password!')
        request.session['email'] = email
        request.session['id'] = user.id
        request.session['username'] = user.username
        return redirect('/homepage?msg=You are logged in successfully')


def logout(request):
    try:
        del request.session['email']
        del request.session['full_name']
        del request.session['id']
        return redirect('loginpage')
    except:
        return redirect('loginpage')


def forgotpassword(request):
    return render(request, 'forgotpassword.html')


def confirm_email(request):
    if request.POST:
        email = request.POST['email']
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return redirect('/forgotpassword?msg=Email does not exist!')
        return render(request, 'setpasswordpage.html', {'data': user})


def setpassword(request):
    if request.POST:
        id = request.POST['user']
        password = request.POST['password']
        try:
            user = Users.objects.get(id=id)
        except Users.DoesNotExist:
            return redirect('/forgotpasswordpage?msg=Something went wrong!')
        user.password = password
        user.save()
        return redirect('/loginpage?msg=Password changed successfully!')

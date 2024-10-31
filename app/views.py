from django.shortcuts import render, redirect
from .models import Users, Income, Expnese
import json
from django.db.models import Sum

# Create your views here.


def index(request):
    return render(request, 'index.html')


def homepage(request):
    user = Users.objects.get(id=request.session.get('id'))
    income_data = Income.objects.filter(user=user).values(
        'month').annotate(total_income=Sum('amount')).order_by('month')
    expense_data = Expnese.objects.filter(user=user).values(
        'month').annotate(total_expense=Sum('amount')).order_by('month')
    income_months = [data['month'] for data in income_data]
    income_amounts = [data['total_income'] for data in income_data]
    expense_months = [data['month'] for data in expense_data]
    expense_amounts = [data['total_expense'] for data in expense_data]
    # income_months_example = ['January', 'February', 'March']  # Example data
    # income_amounts_example = [500, 700, 800]  # Example data
    # expense_months_example = ['January', 'February', 'March']  # Example data
    # expense_amounts_example = [300, 450, 600]  # Example data
    context = {
        'msg': request.GET.get("msg", ""),
        'income_months': json.dumps(income_months),
        'income_amounts': json.dumps(income_amounts),
        'expense_months': json.dumps(expense_months),
        'expense_amounts': json.dumps(expense_amounts),
    }
    return render(request, 'homepage.html', context)


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


def incomepage(request):
    msg = request.GET.get("msg", "")
    incomes = Income.objects.filter(user=request.session.get('id'))
    return render(request, 'incomepage.html', {"msg": msg, 'incomes': incomes})


def add_income(request):
    if request.POST:
        month = request.POST['month']
        amount = request.POST['amount']
        if request.session.get('id'):
            user = Users.objects.get(id=request.session.get('id'))
            if Income.objects.filter(user=user, month=month).exists():
                return redirect('/incomepage?msg=Income for this month already exists')
            Income.objects.create(user=user, month=month, amount=amount)
            return redirect('/incomepage?msg=Income added successfully')
        return redirect('/loginpage?msg=Please try again.')
    return redirect('/loginpage?msg=Something went wrong')


def addexpensepage(request):
    msg = request.GET.get("msg", "")
    user = Users.objects.get(id=request.session.get('id'))
    expenses = Expnese.objects.filter(user=user).all()
    return render(request, "addexpensepage.html", {"msg": msg, 'expenses': expenses})


def addexpense(request):
    if request.POST:
        month = request.POST['month']
        amount = request.POST['amount']
        note = request.POST['note']
        user = Users.objects.get(id=request.session.get('id'))
        Expnese.objects.create(user=user, month=month,
                               amount=amount, note=note)
        return redirect("/addexpensepage?msg=Expense added successfully")
    return redirect("/addexpensepage?msg=Please try again")


def profilepage(request):
    msg = request.GET.get("msg", "")
    if request.session.get('email'):
        user = Users.objects.get(id=request.session.get('id'))
        return render(request, 'profilepage.html', {'msg': msg, 'user': user})
    return redirect('loginpage?msg=Something went wrong! Try again.')


def update_profile(request):
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        try:
            user_id = request.session.get('id')
            Users.objects.filter(id=user_id).update(
                username=username, email=email)
            return redirect('/profilepage?msg=Profile updated successfully')
        except Exception as e:
            print(e)
            return redirect('loginpage?msg=Something went wrong! Try again.')
    return redirect('loginpage?msg=Something went wrong! Try again.!')


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

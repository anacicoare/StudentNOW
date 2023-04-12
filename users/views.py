from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from django.http import HttpResponse
from .models import Student

mystudent = Student.objects.get(id=1)
        
student = {
           "name" : "Maria Popescu",
           "points" : 489,
           "email" : "example@gmail.com",
           "password" : "none",
           "username" : "no username"
        }


def withPoints(request):
    return render(request, 'users/with-points.html', {'student': student})

def withoutPoints(request):
    return render(request, 'users/without-points.html', {'student': student})

def homePage(request):
    return render(request, 'users/home.html', {'student': student})

def home(request):
    return render(request, 'users/pages-login.html', {'student': student})

def registerPage(request):
    return render(request, 'users/pages-register.html', {'student': student})

def usersAccount(request):
    return render(request, 'users/users-account.html', {'student' : student})


def collegeFee(request):
    return render(request, 'users/college-fee.html', {'student': student})

def usersCards(request):
    return render(request, 'users/users-cards.html', {'student' : student})

def userPointTransactions(request):
    return render(request, 'users/user-point-transactions.html', {'student': student})

def firstYear(request):
    return render(request, 'users/first-year.html', {'student': student})

def menu(request):
    return render(request, 'users/menu.html')

def tableReservation(request):
    return render(request, 'users/table-reservation.html', {'student': student})

def pickup(request):
    return render(request, 'users/pickup.html', {'student': student})

def wantLessons(request):
    return render(request, 'users/want-lessons.html', {'student': student})

def regieMarketplace(request):
    return render(request, 'users/regie-marketplace.html', {'student': student})

def calendar(request):
    return render(request, 'users/calendar.html', {'student': student})

def giveLessons(request):
    return render(request, 'users/give-lessons.html', {'student': student})

def modify(request):
    student["name"] = "Ana Cicoare"
    student["email"] = "anacicoare03@gmail.com"
    student['password'] = "anamaria1234"
    student['points'] = 0
    student['username'] = "anacicoare03"

def update_points(request):
    student["points"] += 100
    return render(request, 'users/user-point-transactions.html', {'student': student})
    
def redirect_view(request):
    return redirect(request, 'users/user-point-transactions.html', {'student': student})

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


def showMessage(request):
    return HttpResponse("Hello Geeks")
        
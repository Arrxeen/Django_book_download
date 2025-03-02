
from django.shortcuts import redirect 
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy


class CustomLogoutView(LogoutView):
    next_page = 'login'

class CustomLoginView(LoginView):
    template_name = 'regiter/login.html'
    next_page = 'book_list'

class RegisterView(CreateView):
    template_name = 'regiter/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form): 
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy('book_list'))
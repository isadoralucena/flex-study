from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def register(request):
    if(request.method == 'GET'):
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        
        if not password == password_confirmation: 
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/users/register') 
        
        user = User.objects.filter(username = username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe')
            return redirect('/users/register') 
        
        try:
            User.objects.create_user(
                username = username,
                password = password
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
            return redirect('/users/login')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no servidor')
            return redirect('/users/register')
        
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Usuário logado!')
            return redirect('/flashcards/create_flashcard')
        else:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/users/login')
        
def logout(request):
    auth.logout(request)
    return redirect('/users/login')




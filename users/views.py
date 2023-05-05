from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from bank.models import BankAccount
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.contrib.auth.hashers import get_password_hash_and_salt
import hashlib


def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account created for {username}! You are now able to log in')
      user = form.save() # takes care of creating the user, hashing the password, etc.
      BankAccount.objects.create(owner=user) # creates a new bank account tied to the user
      return redirect('/login/')
  else:
    form = UserRegisterForm()

  context = {
    'form': form
  }
  return render(request, 'users/register.html', context)


def custom_login(request):
    # instead of letting Django handle login, we do it ourself using 
    # raw sql queries in order to introduce the sql injection bug

    if request.method == 'POST':

        # Get the username and password from the form data
        username = request.POST['username']
        password = request.POST['password']
        
        # retrieve the password hash and find out the salt
        stored_hash, salt = get_password_hash_and_salt(password)
        # hash the entered password with the same salt
        entered_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        # Raw SQL query. Here is the SQL injection vulnerability
        query = f"SELECT * FROM auth_user WHERE username='{username}' AND password='{entered_hash}'"
        
        # Execute the query using Django's database connection
        with connection.cursor() as cursor:
          cursor.execute(query)
          user_row = cursor.fetchone()

        # if the query returned a row then the user is there and we can authenticate them
        if user_row is not None:
          user = authenticate(username=username, password=password)
          if user is not None:
            login(request, user)
            return redirect('home')
        
        # If the query didn't return a user row, show an error message
        error = 'Invalid username or password'
    
    else:
        error = None
    
    # Render the login template with the error message (if any)
    return render(request, 'users/login.html', {'error': error})


@login_required
def profile(request):
  return render(request, 'users/profile.html')


def authenticate(username, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT password FROM auth_user WHERE username = %s", [username])
        row = cursor.fetchone()
        if row is not None:
            stored_hash, salt = get_password_hash_and_salt(row[0])
            entered_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            if stored_hash == entered_hash:
                return True
    return False

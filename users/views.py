from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from bank.models import BankAccount
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db import connection
import hashlib
from datetime import datetime
import sqlite3


def custom_register(request):
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']

      # make sure a user does not already exist
      with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM auth_user WHERE username='{username}'")
        user_row = cursor.fetchone()
        if user_row:
          error = 'Username already exists. Please choose a different one.'
          return render(request, 'users/register.html', {'error': error})
      
      # Hash the password
      hashed_password = my_hasher(password)

      current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      
      # Execute raw sql
      with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO auth_user (username, email, password, is_superuser, first_name, last_name, is_staff, is_active, date_joined) VALUES (%s, '', %s, 0, '', '', 0, 1, %s)",
            [username, hashed_password, current_time]
        )

      # Get the newly created user from the database
      # user = authenticate(username=username, password=password)
      query = f"SELECT * FROM auth_user WHERE username='{username}'"

      with connection.cursor() as cursor:
          cursor.execute(query)
          user_row = cursor.fetchone()
      
      # Log in the user and create a new bank account
      if user_row is not None:
        user_id = user_row[0]
        user_obj = User.objects.get(pk=user_id) #User.objects.filter(pk=user_id)[0]
        BankAccount.objects.create(owner=user_obj)
        messages.success(request, f'Account created for {username}! You are now able to log in.')
        return redirect('login')
      
      # If the user wasn't created successfully, show an error message
      else:
        error = 'Error creating user. Please try again.'
    
    else:
      error = None

    return render(request, 'users/register.html', {'error': error})


def custom_login(request):
    # instead of letting Django handle login, we do it ourself using 
    # raw sql queries in order to introduce the sql injection bug

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # username += "	' or '1'='1"
        print(username, password)

        hashed_password = my_hasher(password)

        # Raw SQL query. Here is the SQL injection vulnerability
        query = f"""
          SELECT * FROM auth_user WHERE username='{username}' AND password='{hashed_password}'
        """

        print("This is the query that may contain SQL injection")
        print(query)
        
        # Execute the query using Django's database connection
        con = sqlite3.connect('db.sqlite3')
        con.executescript(query)
        
        q = f"SELECT * FROM auth_user WHERE username='{username}' AND password='{hashed_password}'"
        with connection.cursor() as cursor:
          cursor.execute(q)
          user_row = cursor.fetchone()

        # if the query returned a row then the user is there and we can authenticate them
        if user_row is not None:
          user_id = user_row[0]
          user = User.objects.get(pk=user_id) #User.objects.filter(pk=user_id)[0]
          if user is not None:
            login(request, user)
            return redirect('home')
        
        # If the query didn't return a user row, show an error message
        error = 'Invalid username or password'
    
    else:
        error = None
    
    # Render the login template with the error message (if any)
    return render(request, 'users/login.html', {'error': error})


def my_hasher(password):
  return hashlib.sha256(password.encode('utf-8')).hexdigest()


# @login_required
# def profile(request):
#   return render(request, 'users/profile.html')


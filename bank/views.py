from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from bank.models import BankAccount, Transaction

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
import decimal


def home(request):  
  if request.user.is_anonymous:
    return render(request, 'bank/home.html')
  
  account = BankAccount.objects.get(owner=request.user)
  transactions = Transaction.objects.filter(bank_account=account).order_by('-transaction_date')

  if request.method == 'POST':
    amount = decimal.Decimal(request.POST['amount'])
    transaction_type = request.POST['type']
    if transaction_type == 'deposit':
      account.balance += amount
      account.save()
      transaction = Transaction(bank_account=account, amount=amount)
      transaction.save()
    else:
      account.balance -= amount
      account.save()
      transaction = Transaction(bank_account=account, amount=-amount)
      transaction.save()

  context = {
    'account': account,
    'transactions': transactions
  }
  return render(request, 'bank/home.html', context)

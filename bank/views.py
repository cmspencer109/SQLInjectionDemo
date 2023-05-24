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
    note = request.POST['note']
    transaction_type = request.POST['type']
    if transaction_type == 'Deposit':
      account.balance += amount
      transaction = Transaction(bank_account=account, amount=amount, note=note, type=transaction_type)
    else:
      account.balance -= amount
      transaction = Transaction(bank_account=account, amount=-amount, note=note, type=transaction_type)
    account.save()
    transaction.save()

  context = {
    'account': account,
    'transactions': transactions
  }
  return render(request, 'bank/home.html', context)


@login_required
def send_money(request):
  account = BankAccount.objects.get(owner=request.user)

  if request.method == 'POST':
    amount = decimal.Decimal(request.POST['amount'])
    rec_account_number = request.POST['account_number']
    rec_routing_number = request.POST['routing_number']

    # check that receiving account and routing number exist in the db
    try:
      recipient_account = BankAccount.objects.get(account_number=rec_account_number, routing_number=rec_routing_number)
    except BankAccount.DoesNotExist:
      # if they don't, return an error message
      messages.error(request, 'Invalid account or routing number')
      return redirect('send_money')

    # if they do, create a transaction in both my account and that account
    # my account should be a withdrawal and populate the note field with "Destination account number"
    my_transaction = Transaction.objects.create(
        bank_account=account,
        amount=-amount,
        note=f"Destination account number: {rec_account_number}",
        type="Withdrawal"
    )
    # the receiving account should be the opposite
    recipient_transaction = Transaction.objects.create(
        bank_account=recipient_account,
        amount=amount,
        note=f"Source account number: {account.account_number}",
        type="Deposit"
    )

    # update balances
    account.balance -= amount
    recipient_account.balance += amount
    account.save()
    recipient_account.save()

    messages.success(request, 'Money sent successfully')
    return redirect('home')

  context = {
    'account': account
  }
  return render(request, 'bank/send.html', context)

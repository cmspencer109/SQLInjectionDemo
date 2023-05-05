from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from bank.models import BankAccount, Transaction

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction

# @login_required
# def bank_account_detail(request, account_id):
def home(request):
    return render(request, 'bank/home.html')
    account_id=12355666666
    account = get_object_or_404(BankAccount, pk=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-transaction_date')
    
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        transaction_type = request.POST['type']
        if transaction_type == 'deposit':
            account.current_balance += amount
        else:
            account.current_balance -= amount
        account.save()
        transaction = Transaction(account=account, amount=amount, transaction_type=transaction_type)
        transaction.save()
        return redirect('bank:home', account_id=account.pk)
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/home.html', context)


# {% url 'deposit_or_withdraw' account.pk %}
@login_required
def deposit_or_withdraw(request, account_id):
    account = get_object_or_404(BankAccount, pk=account_id, owner=request.user)
    
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        transaction_type = request.POST['type']
        if transaction_type == 'deposit':
            account.current_balance += amount
        else:
            account.current_balance -= amount
        account.save()
        transaction = Transaction(account=account, amount=amount, transaction_type=transaction_type)
        transaction.save()
        return redirect('bank:bank_account_detail', account_id=account.pk)
    
    return render(request, 'bank/deposit_or_withdraw.html', {'account': account})


def home_other(request):
  # return HttpResponse("Hello, world. You're at the bank index.")
  return render(request, 'bank/home.html')
  if request.user.is_anonymous:
    return render(request, 'bank/home.html')
  
#   context = {
#     'flashcard_decks': FlashcardDeck.objects.filter(author=request.user)
#   }
  context = {}
  return render(request, 'bank/home.html', context)


@login_required
def deposit(request):
  if request.method == 'POST':
    pass
  #   deck = FlashcardDeck() # new flashcard deck object

  #   # process form data
  #   deck.name = request.POST.get('name')
  #   deck.description = request.POST.get('description')
  #   course_id = request.POST.get('course')
  #   deck.course = Course.objects.get(id=course_id)
  #   deck.author = request.user
  
  #   deck.save() # save to database
  #   # messages.success(request, f'Succesfully created deck: {deck.name}!')
  #   return redirect(f'/edit-deck/{deck.id}')

  # context = {
  #   'courses': Course.objects.filter(author=request.user)
  # }
  context = {}

  return render(request, 'bank/create-deck.html', context)


@login_required
def withdraw(request, deck_id):
  if request.method == 'POST':
    pass
  #   flashcard = Flashcard() # new course object

  #   # process form data
  #   flashcard.front = request.POST.get('front')
  #   flashcard.back = request.POST.get('back')
  #   flashcard.flashcard_deck = FlashcardDeck.objects.get(id=deck_id)
  
  #   flashcard.save() # save to database

  # context = {
  #   'deck' : FlashcardDeck.objects.prefetch_related('flashcard_set').get(id=deck_id)
  # }
  context = {}

  return render(request, 'bank/edit-deck.html', context)


from django.db import models
from django.contrib.auth.models import User
import random


class BankAccount(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  account_number = models.BigIntegerField(unique=True)
  routing_number = models.BigIntegerField(unique=True)
  balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

  def save(self, *args, **kwargs):
    if not self.account_number:
      self.account_number = random.randint(10**11, 10**12-1)
    if not self.routing_number:
      self.routing_number = random.randint(10**8, 10**9-1)
    super().save(*args, **kwargs)

  def __str__(self):
    return f"Bank Account {self.account_number}"


class Transaction(models.Model):
  bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
  transaction_date = models.DateTimeField(auto_now_add=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  note = models.CharField(max_length=255, blank=True)
  type = models.CharField(max_length=255, blank=True)

  def __str__(self):
      return f"Transaction of {self.amount} on {self.transaction_date} for {self.bank_account}"

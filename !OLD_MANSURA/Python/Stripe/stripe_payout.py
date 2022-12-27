import stripe

stripe.api_key = "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"

stripe.Topup.create(
  amount=10,
  currency="ca",
  description="Top-up for week of May 31",
  statement_descriptor="Weekly top-up",
)

'''
andrfore_acc_id = "acct_1LrTnAR64MSyIzXb" # WILL HAVE TO GET THE ID 
andrfore_acc_id_card = "card_1LrU9kR64MSyIzXbaHqp0Cna"
transfer = stripe.Transfer.create(
  amount=1,
  currency="usd",
  destination=andrfore_acc_id,
)
print(transfer) # SHOW IT'S FINISHED RUNNING

'''
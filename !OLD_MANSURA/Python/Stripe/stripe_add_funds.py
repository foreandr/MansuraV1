import stripe

stripe.api_key = "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"
trans = stripe.BalanceTransaction.list()
print(trans)
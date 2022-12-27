SET "ACCESS_TOKEN=%1"
SET "RECIEVER=%2"

::curl https://api-m.sandbox.paypal.com/v1/payments/payouts -H "Content-Type: application/json" -H "Authorization: Bearer %ACCESS_TOKEN%" -d '{ "sender_batch_header": { "sender_batch_id": "2014021801", "recipient_type": "EMAIL", "email_subject": "You have money!", "email_message": "You received a payment. Thanks for using our service!" }, "items": [{ "amount": { "value": "9.87", "currency": "USD" }, "sender_item_id": "201403140001", "recipient_wallet": "PAYPAL", "receiver": "%RECIEVER%" } ] }'

curl https://api-m.sandbox.paypal.com/v1/payments/payouts -H "Content-Type: application/json" -H "Authorization: Bearer %ACCESS_TOKEN%" -d "{ \"sender_batch_header\": { \"sender_batch_id\": \"2014021805\", \"recipient_type\": \"EMAIL\", \"email_subject\": \"You have money!\", \"email_message\": \"You received a payment. Thanks for using our service!\" }, \"items\": [{ \"amount\": { \"value\": \"9.87\", \"currency\": \"USD\" }, \"sender_item_id\": \"201403140001\", \"recipient_wallet\": \"PAYPAL\", \"receiver\": \"%RECIEVER%\" } ] }"

 




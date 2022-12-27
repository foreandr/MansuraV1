::set  CLIENT=%1
::echo %var%


SET "CLIENT_ID=%1"
SET "CLIENT_SECRET=%2"
curl https://api-m.paypal.com/v1/oauth2/token -H "Accept: application/json" -H "Accept-Language: en_US" -u "%CLIENT_ID%:%CLIENT_SECRET%"  -d "grant_type=client_credentials" --output location.json
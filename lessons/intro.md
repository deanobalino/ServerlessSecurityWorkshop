# Introduction and Setup

## Prerequisites

There are a few things you will need to have installed to complete this session. Let's get those done first. 

1. [An Azure Account](https://azure.microsoft.com/en-us/free/)
2. [Python 3.7](https://www.python.org/downloads/) (Tested content in 3.7, 2.7/3.6 may be ok)
3. git
4. [Visual Studio Code](https://code.visualstudio.com/Download) (VSCode)
5. [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
6. [Azure Functions Extension for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
7. [Netcat](http://nmap.org/download.html) (Optional)
8. [ngrok](https://ngrok.com/) (Optional)


## Azure Serverless Primer

Please refer to the presentation for this section of the workshop. 

## Deploying our sample app

**Getting our function code**  
First, we need to grab the function code. In a terminal do the following. 

`git clone https://github.com/deanobalino/ServerlessSecurityWorkshop.git`

cd into the directory  

`cd ServerlessSecurityWorkshop`  

Open VSCode  

`code .`


We need to create a serverless app, let's use the Azure functions extension to do this. 

Please follow along with the instructor to create our function app in Azure. We're going to create two functions today, one python one and another node.js one. 

# Secrets

We all know that storing secrets/environment variables in our code is bad practice right? There are so many reasons for this, mainly that this could get checked into a public git repository. But it could also cause issues if private repositories are open to a wide range of people. 

It also makes deploying through a CI/CD pipeline pretty difficult too when variables are hard coded. 

A quick look at our source code for our function shows that our developers have been pretty lazy. We can see that the `ADMINPASSWORD` is right there in our code in plain text. 

Let's look at moving this out into somewhere more secure. 

## Application Settings
One way to move our environment variables away from our code is to leverage application settings in Azure functions. This is great for variables that aren't secrets. 

We're going to use a combination of this and Azure Key Vault.

## Managed Identities
We're going to achieve this by leveraging managed identities. Managed identities enable us to access azure resources without having to store keys in our code. Exactly what we want.  
Refer to the presentation for an explanation on how this works.

## Key Vault Secrets in Application Settings
We can store our secrets in Azure Key Vault and access them just as we would any other environment variables by using a handy feature of Azure Key Vault. Let's get this setup.

First let's create some local environment variables to make our script a little easier, we'll be using our python function here.

```bash
export functionAppName="<YOUR_FUNCTION_APP_NAME>"
export resourceGroup="slsSecWorkshop"
```
assign a managed identity to our function app. 

`az functionapp identity assign -n $functionAppName -g $resourceGroup`  

Keep hold of the output of this command, we'll need some parameters later. don't worry, if you lose them, we can get store them as environment variables by running the following commands.
```bash
#PrincipalID
export principalId=$(az functionapp identity show -n $functionAppName -g $resourceGroup --query principalId -o tsv)
#TenantID
export tenantId=$(az functionapp identity show -n $functionAppName -g $resourceGroup --query tenantId -o tsv)
```

**Create a key vault**
```bash
export keyvaultname="<YOUR_UNIQUE_KEYVAULT_NAME>"
az keyvault create -n $keyvaultname -g $resourceGroup
```

**Save a secret in the key vault**
```bash
export secretName="ADMINPASSWORD"
az keyvault secret set -n $secretName --vault-name $keyvaultname --value "VERYVERYSECRETPASSWORD"
```

**View the secret**
```bash
az keyvault secret show -n $secretName --vault-name $keyvaultname
```

We'll need to get the secret URL, also referred to as secret identifier to get the secret from the vault. 
```bash
export secretId=$(az keyvault secret show -n $secretName --vault-name $keyvaultname --query "id" -o tsv)
```

We now need to give our managed identity some permissions, by default it has none, so here's how we do that. 
```bash
az keyvault set-policy -n $keyvaultname -g $resourceGroup --object-id $principalId --secret-permissions get
```

We can view the policies added by using the following command. It's stored in the `properties.accessPolicies` attribute.  
```bash
az keyvault show -n $keyvaultname -g $resourceGroup
```

As I said earlier, we're going to use application settings to reference our key vault secrets. Azure functions takes care of this for us. We just need to include our app settings with a certain syntax. Something like the following: 

`@Microsoft.KeyVault(SecretUri=https://<KEY_VAULT_NAME>.vault.azure.net/secrets/ADMINPASSWORD/11112222eeee33334444ffffhhhh9999).`

It is possible to do this via the command line, but I had some issues escaping characters to include the syntax. Something to update later. We'll do this in the Azure Portal.

1. Navigate to Azure Function Apps in the portal by using the search bar
2. Select our function app
3. Click Platform Features
4. Click Function App Settings
5. Click Manage Application Settings
6. Click Add new setting
7. Give the setting a name of ADMINPASSWORD
8. Give the setting a value of our syntax from earlier but using your secret URL/ID
   1. `@Microsoft.KeyVault(SecretUri=https://<KEY_VAULT_NAME>.vault.azure.net/secrets/ADMINPASSWORD/11112222eeee33334444ffffhhhh9999).`


### Using our secret in our code
We can now reference our secret from keyvault in our code and Azure functions will take care of all the hard work for us, basically getting a token from the `MSI_ENDPOINT` 

We can now replace in our code:

```python
ADMINPASSWORD = "VERYVERYSECRETPASSWORD"
```

```python
ADMINPASSWORD=os.environ.get('ADMINPASSWORD')
```

Much better right :-) 



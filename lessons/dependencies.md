# Vulnerable Dependencies

Utilising modules in our code makes us a lot more productive, but they can also make us a lot less secure. Incorectly auditing our environment for vulnerable dependencies can leave us wide open to an attack.

Dependency trees can get pretty deep, especially with NPM so we need to make sure we know what we're installing.

We'll look at our Node.js function for this module. 

Navigate to the function directory  
`cd src/slsSecJs`

Install our dependencies  
`npm install`

You should see in the output that there is a critical vulnerability in one of our modules. This is using `npm audit` under the hood. 

W can run this command ourselves to check. This is something we should also include in our build pipelines. 

`npm audit`  

You will see details about the vulnerability in `node-serialize`. For details on how to exploit this vuln, the injection lesson in the OWASP DVSA teaches this. 

## Other tools

### OWASP Dependency Check
We can also leverage tools such as OWASP Dependency check. This is a free tool to help us check this...

Install dependency check from [here](https://jeremylong.github.io/DependencyCheck/dependency-check-cli/index.html).

Then we can run the following from our `/src/slsSecJs` directory.

`dependency-check --project "slsSecJs" --scan "."`

And then access the report by first running our http server: 

`python -m SimpleHTTPServer 80`

and then accessing: 

[http://localhost/dependency-check-report.html](http://localhost/dependency-check-report.html)

Here we can also see the node-serialize dependency. 

### Snyk
Snyk is a popular commercial option for checking vulnerable dependencies. It has a free tier for open source projects. We won't cover it in this session but it's worth checking out. Some resources:  

- [Snyk.io](https://snyk.io/)
- [Snyk Azure Devops Plugin](https://marketplace.visualstudio.com/items?itemName=Snyk.snyk-security-scan)


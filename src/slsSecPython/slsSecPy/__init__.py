import logging

import azure.functions as func
import os
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    ADMINPASSWORD = "VERYVERYSECRETPASSWORD"
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')
    age = req.params.get('age')
    email = req.params.get('email')
    dob = req.params.get('dob')

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        #Create a JSON Object
        data = {
            "name" : name,
            "age" : age,
            "email" : email,
            "dob" : dob
        }
        json_data = json.dumps(data)
        print('writing file with data: {}'.format(json_data))
        #use os.system to write the file using the name
        os.system('echo "{}" >> /tmp/{}'.format(json_data,name))
        
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

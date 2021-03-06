import json
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from skatebetterapi.models import Skater
from rest_framework import status

@csrf_exempt
def login_user(request):

    req_body = json.loads(request.body.decode()) 
    # if the request is an HTTP POST, try to pull out the relevant info
    if request.method == 'POST':
        #  built in method to authenticate
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticated_user = authenticate(username=username, password=password)
        # if authentication was successful, resond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')
        # if bad login details were provided and user can't log in
        else: 
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_user(request):
    #handles creation of a new gamer for authentification
    # load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())
    # create a new user by invoking the 'create_user' helper method on django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )
    # & save teh extra info in the Skater table
    skater = Skater.objects.create(
        user=new_user,
        fav_skater=req_body['fav_skater'],
        fav_video=req_body['fav_video'],
        goofy=req_body['goofy'],
        handle=req_body['handle']
    )
    # commit the User to the database via Skater, save them both 
    skater.save()
    # use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)
    # return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)
from users.models import User
from rest_framework.authtoken.models import Token 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . serializers import UserSerializer
from django.shortcuts import get_object_or_404


@api_view(["POST"])
def signUp(req):
    serializer = UserSerializer(data = req.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(name = req.data['name'])
        user.set_password(req.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user = user)
        return Response({
            'message':'New user has been created.',
            'status':'success',
            'data':{
                'token':token.key,
                'data':serializer.data
            }
        })
    else:
        return Response({
            'Message':'An error occurred',
            'status':'error',
            'data':serializer.errors
        })


@api_view(["POST"])
def login(req):
    user = get_object_or_404(User, email = req.data['email'])
    if user.check_password(req.data['password']):
        token, created = Token.objects.get_or_create(user = user)
        serializer = UserSerializer(instance = user)
        return Response({
            'message':'Logged in successfully',
            'status':'success',
            'data':{
                'token':token.key,
                'data':serializer.data
            }
        })
    else:
        return Response({
            'Message':'An error occurred',
            'status':'error',
            'data':serializer.errors
        })  



@api_view(["GET"])
def getUsers(req):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response({
        'Message':'Fetched Successfully',
        'status':'success',
        'data':serializer.data
    })  
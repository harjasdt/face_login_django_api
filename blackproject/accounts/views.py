from django.shortcuts import render

# Create your views here.
# accounts/views.py
    #importing base64 module
import base64
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer,StockSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated

import face_recognition
import os
import cv2
import pickle
from PIL import Image, ImageTk

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # filepath="../media/test/base.txt"
            # f = open(filepath, "w")
            # f.write(request.data.get('image'))
            # f.close()
            # convert_64_to_image(filepath)
            # capture = cv2.imread("../media/test/image.jpg")
            
            # add(capture,request.data.get('username'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# accounts/views.py
def add(img,name):
    embeddings = face_recognition.face_encodings(img)[0]
    file = open(os.path.join('../media/registered', '{}.pickle'.format(name)), 'wb')
    pickle.dump(embeddings, file)


from .models import CustomUser

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('email')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
# accounts/views.py


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_face_check(request):
    if request.method == 'POST':
        try:
            filepath="../media/test/base.txt"
            f = open(filepath, "w")
            f.write(request.data.get('image'))
            f.close()
            convert_64_to_image(filepath)
            capture = cv2.imread("../media/test/image.jpg")
            ans=recognize(capture,"../media/registered")
            # Delete the user's token to logout
            
            # return Response({'message': "true"}, status=status.HTTP_200_OK)
            return Response({'message': ans}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def convert_64_to_image(filepath):
    #open file with base64 string data
    file = open(filepath, 'rb')
    encoded_data = file.read()
    file.close()
    #decode base64 string data
    decoded_data=base64.b64decode((encoded_data))
    #write the decoded data back to original format in  file
    img_file = open('../media/test/image.jpg', 'wb')
    img_file.write(decoded_data)
    img_file.close()

def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces(
            [embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return True
    else:
        return False

from django.http import HttpResponse

def test(request):
    return HttpResponse("<h1>Page was found</h1>")
    

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def alldata(request):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(email=request.data.get('email'))
            # Delete the user's token to logout
            data={
                "user":user.username,
                "email":user.email,
                # "password":user.password,
                "avalcash":user.avalcash,
                "investedcash":user.investedcash,
                "profit":user.profit
            }
            
            # return Response({'message': "true"}, status=status.HTTP_200_OK)
            return Response({'message': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@api_view(['POST'])
def add_stock(request):
    if request.method == 'POST':
        serializer = StockSerializer(data=request.data)
        user = CustomUser.objects.get(email=request.data.get('email'))
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
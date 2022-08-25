from django.shortcuts import render, get_object_or_404
from django.contrib.auth import models, authenticate, login
from django.contrib.auth.models import User
from rest_framework import response
from django.http import HttpResponse, JsonResponse, request  # 1
from django.views.decorators.csrf import csrf_exempt  # 2
from rest_framework.parsers import DataAndFiles, JSONParser  # 3
from rest_framework.response import Response
import jwt
import datetime
from rest_framework.exceptions import AuthenticationFailed


from rest_framework.views import APIView
from rest_framework import status

from . import models
from . import serializers


class LoginView(APIView):
    def get(self, request):
        return Response({"message":"its working!"})

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        return Response({"Username": username, "Password": password})

    def post_(self, request):
        username = request.data['username']
        password = request.data['password']

        if username is None or password is None:
            raise AuthenticationFailed("Username or Password cannot be empty!")

        user = authenticate(request, username=username, password=password)
        print("user", user)

        if not user:
            raise AuthenticationFailed("Username or Password invalid!")

        login(user=user)

        payload = {
            'id': user.barberId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class BarbersView(APIView):
    def get(self, request):
        barbers = models.Barber.objects.all()
        serializer = serializers.BarberSerializer(barbers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def validate_password(self, password, confirm_password):
        if password != confirm_password:
            raise Exception("Passwords does not match!")
        return password

    def post(self, request):
        serializer = serializers.BarberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # create user profile for the barber. 
        # Todo: Most probably not the best way
        username = serializer.validated_data.get('email_address')
        if (User.objects.filter(username=username).exists()):
            raise Exception("Username already exists!")
        
        data = request.data
        password = self.validate_password(data.get('password'), data.get('confirm_password'))
        user = User.objects.create(username=username)
        user.set_password(password)

        # saving both barber and user account.
        serializer.save()
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BarberView(APIView):
    def get(self, request, id):
        barber = get_object_or_404(models.Barber, national_id=id)
        serializer = serializers.BarberSerializer(barber)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        barber = get_object_or_404(models.Barber, national_id=id)
        serializer = serializers.BarberSerializer(barber, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def delete(self, request, id):
        barber = get_object_or_404(models.Barber, national_id=id)
        barber.delete()
        return Response({"message": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        barber = get_object_or_404(models.Barber, national_id=id)
        serializer = serializers.BarberSerializer(barber, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def get(self, request):
    #     token = request.COOKIES.get('jwt')

    #     if not token:
    #         raise AuthenticationFailed("unauthorised")

    #     try:
    #         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    #     except jwt.ExpiredSignatureError:
    #         raise AuthenticationFailed("session expired")

    #     user = models.Barber.objects.get(barberId=payload['id'])

    #     serializer = BarberSerializer(user)
    #     return Response(serializer.data)

    

class OneBarberView(APIView):
    def get_object(self, request):
        try:
            token = request.COOKIES.get('jwt')

            if not token:
                raise AuthenticationFailed("unauthorised")

            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("session expired")

            user = models.Barber.objects.get(barberId=payload['id'])

            return user

        except models.Barber.DoesNotExist:
            return Response("wakadhakwa", status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        obj = self.get_object(request)
        serializer = serializers.BarberSerializer(obj)

        return Response(serializer.data)

    def put(self, request):

        obj = self.get_object(request)
        serializer = serializers.BarberSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("corrupted data", status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        all = self.get_object(request)
        all.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

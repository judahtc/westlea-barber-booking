from django.shortcuts import render
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

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = models.Barber.objects.filter(email=email).first()

        data = request.data

        if user is None:
            raise AuthenticationFailed('User not found!')

        if user.password != password:
            raise AuthenticationFailed("incorrect password")

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


class BarberView(APIView):
    def get(self, request):
        barbers = models.Barber.objects.all()
        barber_serializer = serializers.BarberSerializer(barbers, many=True)
        return Response(barber_serializer.data, status=status.HTTP_200_OK)

    
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

    # def post(self, request):
    #     barber_serializer = serializers.BarberSerializer(data=request.data)
    #     if barber_serializer.is_valid():
    #         barber_serializer.save()
    #         return Response(barber_serializer.data)
    #     else:
    #         return Response(barber_serializer.error_messages)


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

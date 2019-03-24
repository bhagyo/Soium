from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

import csv, io, re
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from .models import Sign, RReading
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, RReadingSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
            else:
                raise AuthenticationFailed(detail='Password did not match', code=HTTP_401_UNAUTHORIZED)
            return Response({'message': 'User logged in'}, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RReadingAPIView(CreateAPIView):
    queryset = RReading.objects.all()
    serializer_class = RReadingSerializer


class RReadingListAPIView(ListAPIView):
    queryset = RReading.objects.all()
    serializer_class = RReadingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user__id',)


class RReadingCSVAPIView(CreateAPIView):
    queryset = RReading.objects.all()
    serializer_class = RReadingSerializer


def CSVFileUpload(request):
    if request.method == 'GET':
        csv_file = request.FILES['uploadFile']
        decoded_file = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(decoded_file)
        next(io_string)   #for skipping the very first line

        for column in csv.reader(io_string, delimiter='"', quotechar="|"):
            _, created = RReading.objects.update_or_create(
                user = column[0],
                intensity = column[1],
                level = column[2]
            )
        context = {}
        return render(request,"csvUpload.html",context)

'''
            info = line[0].split(',')
            validationFlage = True
            validationFlage = ipCheck(info)
            if validationFlage == True:
                validationFlage = circuitFormatCheck(info)

            if validationFlage == False:
                print(info)
            else:
                cus = RReading(user=info[0], level=info[1], intensity=[2])
                print(cus)
                cus.save()
        return HttpResponse('its  done pls check the database')

        return render(request,"csvUpload.html")
'''
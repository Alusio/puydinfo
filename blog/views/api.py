import json
import os

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets

from blog.models import Spectacle, Data
from blog.serializers import UserSerializer, GroupSerializer, DataSerializer


def api(request, id):
    test = {}
    if id == "version":
        test = settings.APP_VERSION_NUMBER
    if id == "prog":
        with open(os.path.join(settings.BASE_DIR, "templates/show.json")) as json_file:
            test = json.load(json_file)
    if id == "resto":
        with open(os.path.join(settings.BASE_DIR, "templates/restaurant.json")) as json_file:
            test = json.load(json_file)
    if id == "info":
        with open(os.path.join(settings.BASE_DIR, "templates/freq.json")) as json_file:
            test = json.load(json_file)
    return JsonResponse(test, safe=False)

def getdata(request):
    results = Spectacle.objects.all()
    jsondata = serializers.serialize('json', results)
    return HttpResponse(jsondata)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all().order_by('date')
    serializer_class = DataSerializer

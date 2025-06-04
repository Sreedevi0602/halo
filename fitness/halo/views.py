from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Class
from .serializers import ClassSerializer

# Create your views here.
@api_view(['GET'])
def class_list_view(request):
    classes = Class.objects.filter(datetime__gte=timezone.now())
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)
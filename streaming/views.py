from django.shortcuts import render
from rest_framework import viewsets
from .models import Stream
from .serializers import StreamSerializer


class StreamViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
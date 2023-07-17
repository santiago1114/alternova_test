from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import action
from .models import Stream, Type, Genre, UserStreamDetails
from .serializers import (StreamSerializer, StreamDetailViewSet, 
                          TypeSerializer, GenreSerializer, UserRegistrationSerializer)
import random


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    
    def post(self, request):
      
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Create the user object without saving it
            user = User(**serializer.validated_data)
            
            # Extract the password from the data
            password = serializer.validated_data.pop('password', None)
            
            if password:
                # Set and encrypt the password using Django's built-in method
                user.set_password(password)

            # Save the user object
            user.save()
            
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TypeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Type model
    """
    permission_classes=[IsAuthenticated] 
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class GenreViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Genre model
    """
    permission_classes=[IsAuthenticated] 
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class StreamViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Stream model
    """
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes=[IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['genre']
    search_fields = ['name', 'genre__name', 'type__name']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 25
    ordering_fields = ['name', 'genre__name', 'type__name', 'score']
    ordering = ['name']  # You can set the default sorting here
    ordering_param = 'sort'
    
    def get_serializer_class(self):
        if self.action == 'list':  # Check if it's a GET request for a single item
            return StreamDetailViewSet
        return super().get_serializer_class()
    
    def create(self, request):
        serializer = StreamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        try:
            # Get streaming details from user
            user_streaming_details = UserStreamDetails.objects.get(user=request.user, stream=instance)
            if user_streaming_details.is_viewed:
                return Response(serializer.data)
            user_streaming_details.is_viewed = True
            user_streaming_details.save()
        except UserStreamDetails.DoesNotExist:
            # If doesn't exists stream details create one
            UserStreamDetails.objects.create(user=request.user, stream=instance, is_viewed=True)
        
        instance.views += 1
        instance.save()
       
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = super().get_queryset()

        # If you want to allow sorting in reverse, you can do this:
        reverse_order = self.request.query_params.get('reverse', False)
        if reverse_order in ['1', 'true', 'True']:
            reverse_order = True
        else:
            reverse_order = False

        # Apply sorting
        ordering = self.request.query_params.get(self.ordering_param)
        if ordering in self.ordering_fields:
            if reverse_order:
                ordering = f'-{ordering}'
            queryset = queryset.order_by(ordering)

        return queryset
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            try:
                user_streaming_details = UserStreamDetails.objects.get(user=request.user, stream=instance)
                if user_streaming_details.is_scored:
                    return Response(serializer.data)
                user_streaming_details.is_scored = True
                user_streaming_details.save()
            except UserStreamDetails.DoesNotExist:
                # If doesn't exists stream details create one
                UserStreamDetails.objects.create(user=request.user, stream=instance, is_scored=True)
        
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def random_stream(self, request):
        queryset = self.get_queryset()
        
        # Check if the queryset is not empty
        if queryset.exists():
            random_stream = random.choice(queryset)
            serializer = self.get_serializer(random_stream)
            return Response(serializer.data)
        else:
            return Response({'detail': 'No streams available.'}, status=404)
        
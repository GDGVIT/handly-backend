from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import (
    Collections,
    HandwritingInputLogger, InputFile,
)
from .serializers import (
    CollectionSerializer,
    HandwritingInputSerializer, InputFileSerializer,
)
from accounts.models import OneSignalNotifications
from .tasks import output_file_proccessor, generateUrl
import boto3

class CollectionsView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser]

    def check_permissions_update(self, request, id):
        collection = Collections.objects.filter(user=request.user).filter(id=id)
        return (True, collection if collection.count() == 1 else False)

    def get(self, request):
        queryset = Collections.objects.filter(user=request.user)
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def put(self, request):
        id = request.data['id']
        status, queryset = self.check_permissions_update(request, id)
        if status:
            serializer = CollectionSerializer(queryset[0], data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=203)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({
                'message': 'Object/Permission doesn\'t exisit\'s '
            }, status=404)

    def delete(self, request):
        id = request.data['id']
        status, queryset = self.check_permissions_update(request, id)
        if status:
            queryset.delete()
            return Response(status=204)
        else:
            return Response({
                'message': 'Object/Permission doesn\'t exisit\'s '
            }, status=404)


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass  # status

    def post(self, request):
        serializer = InputFileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            serializer1 = HandwritingInputSerializer(data=request.data)
            if serializer1.is_valid():
                serializer1.save(input_file=InputFile.objects.filter(id=serializer.data['id'])[0])
            else:
                return Response({"errors":serializer1.errors}, status=400)
            try:
                player_id = request.user.onesignalnotifications.player_id
            except:
                player_id = ''
            print(serializer1.data['id'], player_id)
            output_file_proccessor(serializer1.data['id'], serializer.data['file'], player_id)
            return Response(serializer1.data, status=201)
        else:
            return Response({"errors":serializer.errors}, status=400)


class FileUploadPresignView(APIView):
    def post(self,request):
        key = request.data.get('key',None)
        if key is not None:
            return Response(generateUrl(key),status=200)
        return Response(status=400)
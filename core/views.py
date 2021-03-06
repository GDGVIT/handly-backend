from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import (
    Collections,
    HandwritingInputLogger,
    )
from .serializers import (
    CollectionSerializer,
    HandwritingInputSerializer,
)
from accounts.models import OneSignalNotifications
from .tasks import output_file_proccessor
class CollectionsView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser]
    def check_permissions_update(self,request,id):
        collection = Collections.objects.filter(user=request.user).filter(id=id)
        return (True,collection if collection.count()==1 else False)

    def get(self,request):
        queryset = Collections.objects.filter(user=request.user)
        serializer = CollectionSerializer(queryset,many=True)
        return Response(serializer.data,status=200)

    def post(self,request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)

    def put(self,request):
        id = request.data['id']
        status, queryset = self.check_permissions_update(request,id)
        if status:
            serializer = CollectionSerializer(queryset[0],data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=203)
            else:
                return Response(serializer.errors,status=400)
        else:
            return Response({
                'message':'Object/Permission doesn\'t exisit\'s '
            },status=404)
    
    def delete(self,request):
        id = request.data['id']
        status, queryset = self.check_permissions_update(request,id)
        if status:
            queryset.delete()
            return Response(status=204)
        else:
            return Response({
                'message':'Object/Permission doesn\'t exisit\'s '
            },status=404)


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        pass #status

    def post(self,request):
        serializer1 = HandwritingInputSerializer(data=request.data)
        if serializer1.is_valid():
            serializer1.save()
            try:
                player_id = request.user.onesignalnotifications.player_id
            except:
                player_id = ''
            output_file_proccessor(serializer1.data['id'],serializer1.data['input_file'],player_id)
            return Response(serializer1.data,status=201)
        else:
            return Response(serializer1.errors,status=400)
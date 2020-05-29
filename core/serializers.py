from rest_framework import serializers
from .models import(
    Collections,
    HandwritingInputLogger,
    OutputFiles
)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        exclude = ['user'] 


class HandwritingInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandwritingInputLogger
        fields = '__all__'

class OutputFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputFiles
        exclude =  ['input_details']


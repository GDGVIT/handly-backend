from django.db.models import fields
from rest_framework import serializers
from .models import (
    Collections,
    HandwritingInputLogger,
    OutputFiles,
    InputFile
)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        exclude = ['user']


class HandwritingInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandwritingInputLogger
        exclude = ['input_file']



class InputFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputFile
        fields = '__all__'


class OutputFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputFiles
        exclude = ['input_details']


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputFiles
        fields = '__all__'
from rest_framework import serializers

from .models import Content


class ImportContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('id',
                  'url',
                  'type',
                  'parentId',
                  'date',
                  'size',
                  )


class ExportContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('id',
                  'url',
                  'type',
                  'date',
                  'size',
                  'parentId',
                  'children'
                  )
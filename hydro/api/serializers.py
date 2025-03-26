from rest_framework import serializers
from divert.models import GeoPoint

class GeoSerializer(serializers.ModelSerializer):
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()

    class Meta:
        model = GeoPoint
        fields = ['id', 'latitude', 'longitude', 'pod', 'podType',
            'podRate', 'units', 'podStorage', 'owner', 'faceValueAF',
            'maxDiversionFlow', 'unitsFlow', 'status']

'''
from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'completed']

class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title', 'memo', 'created', 'completed']
'''

        
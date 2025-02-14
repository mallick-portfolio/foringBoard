from .models import Project, Task
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'owner']
        read_only_fields = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)



class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.ReadOnlyField(source='assigned_to.id')
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['assigned_to']

    def create(self, validated_data):
        print("self", self)
        validated_data['assigned_to'] = self.context['request'].user
        return super().create(validated_data)

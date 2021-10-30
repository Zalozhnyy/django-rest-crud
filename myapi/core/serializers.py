from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    # creator = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task_name', 'task_description', 'task_end', 'executors', 'creator']

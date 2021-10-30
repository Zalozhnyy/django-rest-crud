from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import permissions, generics, status
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from .serializers import (
    UserSerializer, TaskSerializer)
from .models import Task


def get_user_id(token):
    return Token.objects.get(key=token).user_id


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class TaskAPIView(generics.GenericAPIView):
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        '''
        :param request:
        :return:
        '''
        task = request.data
        task.update({'creator': get_user_id(request.auth.key)})

        serializer = self.serializer_class(data=task)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskAPIViewDetailed(generics.GenericAPIView):
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskSerializer

    def get(self, request, pk):
        '''
        :param request:
        :param pk: user id
        :return:
        '''
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'error': f'user_id={pk} not exists'}, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(executors=pk)

        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        '''
        Update task with id=pk
        :param request:
        :param pk: task id
        :return:
        '''
        try:
            instance = Task.objects.get(pk=pk)
            if get_user_id(request.auth.key) != instance.creator_id:
                return Response({'error': f'you cant update this task'}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({'error': f'task with id={pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        task = request.data
        serializer = self.serializer_class(data=task)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, task)

        return Response(status=status.HTTP_200_OK)


class DeleteTaskAPIView(generics.GenericAPIView):
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskSerializer

    def delete(self, request, pk):
        user_id = get_user_id(request.auth.key)

        try:
            instance = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'error': f'task with id={pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if user_id == instance.creator_id:
            instance.delete()
        else:
            return Response({'error': f'you cant delete this task'}, status=status.HTTP_403_FORBIDDEN)

        return Response(f'task with id={pk} deleted', status=status.HTTP_200_OK)

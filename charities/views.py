from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)


class BenefactorRegistration(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = BenefactorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CharityRegistration(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CharitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsCharityOwner, ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)


class TaskRequest(APIView):
    permission_classes = (IsBenefactor,)

    def get(self, request, task_id, **kwargs):
        task = get_object_or_404(Task, id=task_id)
        if task.state != Task.TaskStatus.PENDING:
            message = 'This task is not pending.'
            return Response(data={'detail': message}, status=status.HTTP_404_NOT_FOUND)

        task.assign_to_benefactor(request.user.benefactor)

        return Response(data={'detail': 'Request sent.'}, status=status.HTTP_200_OK)


class TaskResponse(APIView):
    permission_classes = (IsCharityOwner,)

    def post(self, request, task_id):
        response = request.data.get('response')
        if response not in ['A', 'R']:
            message = 'Required field ("A" for accepted / "R" for rejected)'
            return Response(data={'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        task = get_object_or_404(Task, id=task_id, charity=request.user.charity)
        if task.state != Task.TaskStatus.WAITING:
            message = 'This task is not waiting.'
            return Response(data={'detail': message}, status=status.HTTP_404_NOT_FOUND)

        task.response_to_benefactor_request(response)

        return Response(data={'detail': 'Response sent.'}, status=status.HTTP_200_OK)


class DoneTask(APIView):
    permission_classes = (IsCharityOwner,)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, charity=request.user.charity)
        if task.state != Task.TaskStatus.ASSIGNED:
            message = 'Task is not assigned yet.'
            return Response(data={'detail': message}, status=status.HTTP_404_NOT_FOUND)

        task.done()

        message = 'Task has been done successfully.'
        return Response(data={'detail': message}, status=status.HTTP_200_OK)

from calendar import c
from datetime import datetime
import re
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from taskapp.authentication import AdminAuthentication, UserAuthentication, generate_token
from taskapp.models import *


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
            name,email,password,phone number is required
        """
        data = request.data
        validation_arr = [None, ""]

        name = data['name']
        email = data['email']
        password = data['password']
        phone = data['phone']

        if name in validation_arr or email in validation_arr or phone in validation_arr or password in validation_arr:
            return Response({"message": "name,email,password,phone is required"}, status=status.HTTP_400_BAD_REQUEST)

        check_user = User.objects.filter(email=email).first()
        if check_user:
            return Response({"message": "email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone
        )
        token = generate_token({
            "id": user.id
        })
        return Response({"message": "user created successfully", "token": token}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        password = data['password']

        if email in ["", None] or password in ["", None]:
            return Response({"message": "email,password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"message": "email not exists"}, status=status.HTTP_400_BAD_REQUEST)

        if user.password != password:
            return Response({"message": "password is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        token = generate_token({
            "id": user.id
        })
        return Response({"message": "login successfully", "token": token}, status=status.HTTP_200_OK)

class AdminRegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
            name,email,password,phone number is required
        """
        data = request.data
        validation_arr = [None, ""]

        name = data['name']
        email = data['email']
        password = data['password']
        phone = data['phone']

        if name in validation_arr or email in validation_arr or phone in validation_arr or password in validation_arr:
            return Response({"message": "name,email,password,phone is required"}, status=status.HTTP_400_BAD_REQUEST)

        check_user = User.objects.filter(email=email).first()
        if check_user:
            return Response({"message": "email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone,
            is_superuser = True
        )
        token = generate_token({
            "id": user.id
        })
        return Response({"message": "super user created successfully", "token": token}, status=status.HTTP_201_CREATED)

class AdminLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        password = data['password']

        if email in ["", None] or password in ["", None]:
            return Response({"message": "email,password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"message": "email not exists"}, status=status.HTTP_400_BAD_REQUEST)

        if user.password != password:
            return Response({"message": "password is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_superuser != True:
            return Response({"message": "user is not super user"}, status=status.HTTP_400_BAD_REQUEST)

        token = generate_token({
            "id": user.id
        })
        return Response({"message": "login successfully", "token": token}, status=status.HTTP_200_OK)

class TaskView(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = []

    def get(self, request, *args, **kwargs):
        user = request.user
        id = request.data['id']

        if id not in ["", None]:
            task = Task.objects.filter(id=id).first()
            if task is None:
                return Response({"message": "task not exists"}, status=status.HTTP_400_BAD_REQUEST)

            if task.user_id != user.id:
                return Response({"message": "task not exists"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "task found", "task": task.to_dict()}, status=status.HTTP_200_OK)
        else:
            tasks = Task.objects.filter(user_id=user.id)
            return Response({"message": "tasks found", "tasks": [task.to_dict() for task in tasks]}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
            title,content in string
            start_date in the format of yyyy-mm-dd
            end_date in the format of yyyy-mm-dd
            start_time in the format of hh:mm:ss
            end_time in the format of hh:mm:ss
        """

        data = request.data
        user = request.user

        title = data['title']
        content = data['content']
        start_date = data['start_date']
        end_date = data['end_date']
        start_time = data['start_time']
        end_time = data['end_time']

        if title in ["", None] or content in ["", None] or start_date in ["", None] or end_date in ["", None] or start_time in ["", None] or end_time in ["", None]:
            return Response({"message": "title,content,start_date,end_date,start_time,end_time is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", start_date):
            return Response({"message": "start_date is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", end_date):
            return Response({"message": "end_date is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r"^\d{2}:\d{2}:\d{2}$", start_time):
            return Response({"message": "start_time is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r"^\d{2}:\d{2}:\d{2}$", end_time):
            return Response({"message": "end_time is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.create(
                title=title,
                content=content,
                start_date=datetime.datetime.strptime(start_date, "%Y-%m-%d"),
                end_date=datetime.datetime.strptime(end_date, "%Y-%m-%d"),
                start_time=datetime.datetime.strptime(start_time, "%H:%M:%S"),
                end_time=datetime.datetime.strptime(end_time, "%H:%M:%S"),
                user_id=user.id
            )
            return Response({"message": "task created successfully", "task": task.to_dict()}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "task not created","error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
            id is required
            title,content is str
            start_date in the format of yyyy-mm-dd
            end_date in the format of yyyy-mm-dd
            start_time in the format of hh:mm:ss
            end_time in the format of hh:mm:ss
            completed in bool
        """
        data = request.data
        user = request.user
        val_arr = ["",None]
        id = data['id']

        if id in val_arr:
            return Response({"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.filter(id=id).first()
        if task is None:
            return Response({"message": "task not exists"}, status=status.HTTP_400_BAD_REQUEST)

        if task.user_id != user.id:
            return Response({"message": "task not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        title = data['title']
        content = data['content']
        start_date = data['start_date']
        end_date = data['end_date']
        start_time = data['start_time']
        end_time = data['end_time']
        completed = data['completed']

        if title not in val_arr:
            task.title = title

        if content not in val_arr:
            task.content = content
        
        if start_date not in val_arr:
            task.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        
        if end_date not in val_arr:
            task.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        if start_time not in val_arr:
            task.start_time = datetime.datetime.strptime(start_time, "%H:%M:%S")

        if end_time not in val_arr:
            task.end_time = datetime.datetime.strptime(end_time, "%H:%M:%S")

        if completed not in val_arr and completed in [True,False]:
            task.completed = completed

        task.save()
        return Response({"message": "task updated successfully", "task": task.to_dict()}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        id = data['id']

        if id in ["", None]:
            return Response({"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        task = Task.objects.filter(id=id).first()
        if task is None:
            return Response({"message": "task not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if task.user_id != user.id:
            return Response({"message": "task not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        task.delete()
        return Response({"message": "task deleted successfully"}, status=status.HTTP_200_OK)
    
class SearchTask(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
            ?query=<str>&completed=<bool
            query : title search term
            completed : bool
        """
        data = request.query_params
        user = request.user
        val_arr = ["",None]

        query = data['query']
        completed = data['completed']

        task = Task.objects.filter(user_id=user.id)

        if completed in [True, False,'true','false','True','False']:
            task = task.filter(completed=bool(completed))

        if query not in val_arr:
            task = task.filter(title__icontains=query)
            
        return Response({"message": "task found successfully", "task": [task.to_dict() for task in task]}, status=status.HTTP_200_OK)

class AdminTaskView(APIView):
    authentication_classes = [AdminAuthentication]
    permission_classes = []

    def get(self, request):
        """
            user_id=<str>
            completed=<bool>
        """
        data = request.data
        val_arr = ["",None]

        user_id = data['user_id']
        completed = data['completed']

        if user_id in val_arr:
            task = Task.objects.all()
            if completed in [True, False,'true','false','True','False']:
                task = task.filter(completed=bool(completed))
            return Response({"message": "task found successfully", "task": [task.to_dict() for task in task]}, status=status.HTTP_200_OK)
        
        task = Task.objects.filter(user_id=user_id)
        if completed in [True, False,'true','false','True','False']:
            task = task.filter(completed=bool(completed))
        return Response({"message": "task found successfully", "task": [task.to_dict() for task in task]}, status=status.HTTP_200_OK)

class AdminViewUserView(APIView):
    authentication_classes = [AdminAuthentication]
    permission_classes = []

    def get(self, request):
        """
            user_id=<str>
        """
        data = request.data
        val_arr = ["",None]

        user_id = data['id']

        if user_id in val_arr:
            user = User.objects.all()
            return Response({"message": "user found successfully", "user": [user.to_dict() for user in user]}, status=status.HTTP_200_OK)
        
        user = User.objects.filter(id=user_id)
        return Response({"message": "user found successfully", "user": [user.to_dict() for user in user]}, status=status.HTTP_200_OK)



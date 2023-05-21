import json
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import UserDetail, Users

class UsersView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')

        token = auth_header.split(' ')[1]

        try:
            obj = Token.objects.get(key=token)
        except:
            return Response({"status": 403, "message": "Token authentication error."})

        users = Users.objects.all()
        print(users)
        users_data = []
        for user in users:
            user_dict = {}
            user_details = UserDetail.objects.filter(user_id=user)
            detail_list = []
            for user_detail in user_details:
                detail_dict = {}
                
                detail_dict["username"] = user_detail.user_id.username
                detail_dict["date_of_birth"] = user_detail.date_of_birth
                detail_dict["gender"] = user_detail.gender
                detail_dict["mobile"] = user_detail.mobile
                detail_dict["address"] = user_detail.address
                detail_list.append(detail_dict)
            user_dict[user.user_email] = detail_list
            users_data.append(user_dict)

        return Response({"status": 200, "Users Data": str(users_data), "message": "Data find successfully"})


class CeateUserView(APIView):
    def post(self, request, *args, **kwarga):
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        try:
            obj = Token.objects.get(key=token)
        except:
            return Response({"status": 403, "message": "Token authenticated error."})

        data = json.loads(request.body)
        print(data)
        username = data["username"]
        email = data["user_email"]
        password = data["password"]
        date_of_birth = data["date_of_birth"]
        mobile = data["mobile"]
        gender = data["gender"]
        address = data["address"]
       
        if Users.objects.filter(user_email=email).exists():
            return Response({"status": 200, "message": "User Already Exists"})
        
        try:
            user_obj = Users.objects.create(username=username, user_email=email, password=password)
            user_obj.save()

            user_detail = UserDetail.objects.create(user_id=user_obj, date_of_birth=date_of_birth, mobile=mobile, gender=gender, address=address)
            user_detail.save()
        except :
            return Response({"status": 200, "message": "Some issue founded while creating the user"})
            

        return Response({"status": 200, "message": "User Data created successfully"})

class DeleteUserView(APIView):
    def delete(self, request, *args, **kwarga):
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            obj = Token.objects.get(key=token)
        except:
            return Response({"status": 403, "message": "Token authenticated error."})

        data = json.loads(request.body)
        print(data)
        user_id = data["id"]
        print(user_id)
        try:
            if Users.objects.filter(id=user_id).exists():
                Users.objects.filter(id=user_id).delete()
            else:
                return Response({"status": 200, "message": "User not available"})
        except:
            return Response({"status": 200, "message": "Some issue founded while deleting the user"})
        
        return Response({"status": 200, "message": "User Data deleted successfully"})
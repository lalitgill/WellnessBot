from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
import traceback
from users.models import UserRole, User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        #response.data['custom_key'] = 'my_custom_data'

        return response

class CreateUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data = request.data
            app_id = data.get('app_id')
            if get_user_model().objects.filter(email=data.get('email')).exists():
                return Response({'success': 0, 'message': 'Email already exists'})

            if data.get('role') is None:
                return Response({'success': 0, 'message': 'Role not found'})

            user_role = UserRole.objects.get(name=data.get('role'))

            user = get_user_model().objects.create_user(
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                username=data.get('email'),
                organisation_name=data.get('organisation_name'),
                role=user_role
            )
            if data.get('is_active') == True:
                user.is_active = True
                user.save()
            else:
                user.is_active = False
                user.save()

            return Response({'success': True, 'message': 'User created successful'})
        except:
            print(traceback.format_exc())
            return Response({'success': False, 'message': 'user cannot created failed'})

class EditUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data = request.data
            if data.get('id') is None:
                return Response({'success': 0, 'message': 'id not exists'})

            if get_user_model().objects.filter(~Q(id=data.get('id')), email=data.get('email')).exists():
                return Response({'success': 0, 'message': 'Email already exists'})

            if get_user_model().objects.filter( id=data.get('id') ).exists():
                pass
            else:
                return Response({'success': 0, 'message': 'User not exists'})

            user_role = UserRole.objects.get(name=data.get('role'))


            User.objects.filter(id=data.get('id')).update(
                                                        username=data.get('email'),
                                                        email=data.get('email'),
                                                        first_name= data.get('first_name'),
                                                        last_name= data.get('last_name'),
                                                        organisation_name=data.get('organisation_name'),
                                                        role= user_role,
                                                        is_active= data.get('is_active')
                                                        )

            return Response({'success': True, 'message': 'User updated successful'})
        except:
            print(traceback.format_exc())
            return Response({'success': False, 'message': 'user cannot updated failed'})

class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data = request.data
            if get_user_model().objects.filter( id=data.get('id') ).exists():
                pass
            else:
                return Response({'success': 0, 'message': 'User not exists'})

            User.objects.filter(id=data.get('id')).delete()

            return Response({'success': True, 'message': 'User deleted successful'})
        except:
            return Response({'success': False, 'message': 'user cannot deleted failed'})

class ClientUsersList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            users = get_user_model().objects.all()
            data = []
            for user in users:
                #userroles = UserRole.objects.filter(id=user.role)
                data.append({
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role.name,
                    'organisation_name': user.organisation_name,
                    'is_active': user.is_active
                })
            return Response(data)
        except:
            return Response({
                'responseCode': 0,
                'responseMessage': 'Something went wrong'
            })

class UsersDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            userdata = User.objects.filter(id=request.GET.get('id'))
            if len(userdata) == 0:
                return Response({
                    'responseCode': 0,
                    'responseMessage': 'No Data Found'
                })
            userdata = userdata[0]
            DataResponse = {}
            DataResponse['id'] = userdata.id
            DataResponse['first_name'] = userdata.first_name
            DataResponse['last_name'] = userdata.last_name
            DataResponse['email'] = userdata.email
            DataResponse['role'] = userdata.role.name
            DataResponse['organisation_name'] = userdata.organisation_name
            DataResponse['is_active'] = userdata.is_active

            return Response(DataResponse)
        except:
            return Response({
                'responseCode': 0,
                'responseMessage': 'Something went wrong'
            })


class ResetPassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            # get data payload
            data = request.data
            # get the user using uid
            if data['formdata']['current_password'] != data['formdata']['confirm_current_password']:
                return Response({
                    'responseCode': 0,
                    'responseMessage': 'current password and confirm current password does not match'
                })

            user = get_user_model().objects.get(id=data.get('id'))
            user.set_password(data['formdata']['current_password'])
            user.save()
            return Response({'success': True, 'message': 'Password update successful'})
        except:
            return Response({
                'responseCode': 0,
                'responseMessage': 'Something went wrong'
            })
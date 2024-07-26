from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
import datetime
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        #token.set_exp(lifetime=timedelta(days=10))
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['id'] = user.id
        token['organisation_name'] = user.organisation_name
        token['role'] = user.role.name

        return token
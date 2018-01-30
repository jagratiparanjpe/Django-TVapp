from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from django.db.models import Q

User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    # token = CharField(allow_blank=True, read_only=True)
    # username = CharField()
    class Meta:
        model = User
        fields = [
            'username',
        ]

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token'
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    ## validate the username and password and return Token
    # def validate(self, data):
    #     user_obj = None
    #     username = data.get("username", None)
    #     password = data["password"]
    #     if not username:
    #         raise ValidationError("A username is required to login")
    #     user = User.objects.filter(Q(username=username)).distinct()
    #     if user.exists() and user.count() == 1:
    #         user_obj=user.first()
    #     else:
    #         raise ValidationError("This username is not valid")
    #     if not user_obj.check_password(password):
    #         raise ValidationError("Incorrect Credentials")
    #     data["token"] = "SOME RANDOM TOKEN"
    #     return data



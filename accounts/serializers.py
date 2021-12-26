from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=User.Gender.choices, default=User.Gender.UNSET)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'phone',
            'address',
            'gender',
            'age',
            'description',
            'first_name',
            'last_name',
            'email'
        )

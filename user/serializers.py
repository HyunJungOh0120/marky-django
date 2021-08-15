from rest_framework import serializers

from .models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                {'username': 'The username should only contain alphanumeric characters'})

        user = MyUser.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError({
                'email': 'This email is already used'
            })

        return attrs

    def create(self, validated_data):
        """
        Create and return a new user, given the validated data.
        """
        return MyUser.objects.create_user(**validated_data)

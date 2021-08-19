from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, attrs):
        print('🍉', attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        parent = validated_data['parent']

        if parent is None:

            Category.objects.create(
                parent=validated_data['parent']['id'], name=validated_data['name'],
                user=validated_data['user'],
                topic=validated_data['topic'],
                slug=validated_data['slug'])


class ChildSerializer(serializers.ModelSerializer):

    parent = CategorySerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['user', 'topic', 'name', 'parent', 'slug']

    def validate_user(self, user):
        return super().validate(user)

    # def create(self, validated_data):
    #     child = Category.objects.create(
    #         parent=validated_data['parent']['id'], name=validated_data['name'],
    #         user=validated_data['user'],
    #         topic=validated_data['topic'],
    #         slug=validated_data['slug'])

    #     return child

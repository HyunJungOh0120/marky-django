from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from article.models import Article

from .serializers import CategorySerializer
from article.serializers import ArticleSerializer

# Create your views here.


class CategoryAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()

    def get(self, request, id):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        obj = qs.first()

        articles = Article.objects.filter(category=id)
        article_serializer = ArticleSerializer(articles, many=True)
        article_serializer.is_valid(raise_exception=True)

        serializer = self.serializer_class(obj)

        data = {
            "category": serializer.data,
            "articles": article_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, id):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()

        topic = request.data.get('topic')
        name = request.data.get('name')
        user = request.user.id

        data = {
            'topic': topic,
            'name': name,
            'user': user
        }
        serializer = self.serializer_class(instance=obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instance=obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        qs = qs.filter(user=request.user.id)
        if not qs.exists():
            return Response({"message": "You cannot delete this category"})

        obj = qs.first()
        obj.delete()

        return Response({"message": "Category is removed"}, status=status.HTTP_204_NO_CONTENT)


class CategoriesAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()

# per user
    def get(self, request):

        user = request.user.id

        queryset = self.queryset.objects.filter(user=user)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        article = request.data.get('article')
        text = request.data.get('text')
        user = request.user.id

        data = {
            'article': article,
            'text': text,
            'user': user
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        memo = serializer.data

        return Response(memo, status=status.HTTP_201_CREATED)

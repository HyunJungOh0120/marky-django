from article.models import Article
from article.serializers import ArticleSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify.slugify import slugify

from .models import Category
from .serializers import CategorySerializer, ChildSerializer

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
        serializer = self.serializer_class(obj)

        # child
        children = self.queryset.filter(parent=id)
        print(children)
        child_serializer = self.serializer_class(children, many=True)

        article = Article.objects.filter(category=id)

        # has article
        article_serializer = ArticleSerializer(article, many=True)
        data = {
            "category": serializer.data,
            "children": child_serializer.data,
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
        slug = slugify(name)

        data = {
            'topic': topic,
            'name': name,
            'user': user,
            'slug': slug
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


class Node(object):
    def __init__(self, name, size=None):
        self.name = name
        self.children = []
        self.size = size

    def child(self, cname, size=None):
        child_found = [c for c in self.children if c.name == cname]
        if not child_found:
            _child = Node(cname, size)
            self.children.append(_child)
        else:
            _child = child_found[0]
        return _child

    def as_dict(self):
        res = {'name': self.name}
        if self.size is None:
            res['children'] = [c.as_dict() for c in self.children]
        else:
            res['size'] = self.size
        return res


class CategoriesAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()

# per user
    def get(self, request):

        user = request.user.id
        qs = self.queryset.filter(user=user, parent=None)

        serializer = self.serializer_class(qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user.id
        topic = request.data.get('topic')
        name = request.data.get('name')
        action = request.data.get('action', '')
        parent = request.data.get('parent', '')
        slug = slugify(name)

        data = {
            'user': user,
            'topic': topic,
            'name': name,
            'slug': slug,
            'parent': parent
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):

            if action == 'subcategory':
                data = serializer.validated_data
                parent_id = data.get('parent').id

                user = data.get('user')
                qs = Category.objects.filter(id=parent_id)

                if not qs.exists():
                    return Response({"message": "This article doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
                obj = qs.first()

                new_category = Category.objects.create(
                    user=user,
                    topic=topic,
                    name=name,
                    parent=obj,
                    slug=slug
                )
                print('new-category', new_category)
                serializer = ChildSerializer(new_category)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

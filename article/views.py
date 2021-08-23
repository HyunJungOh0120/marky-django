
import base64
import io
import json
import time
from io import BytesIO
from os import fwalk

import cloudinary
import cloudinary.api
import cloudinary.uploader
# import pdfkit
import requests
from bs4 import BeautifulSoup
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from PIL import Image
# from playwright.sync_api import sync_playwright
from rest_framework import generics
from rest_framework import status
from rest_framework import status as res_status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from selenium import webdriver
from slugify import slugify
from user.models import MyUser

from .models import Article
from .serializers import ArticleSerializer

# from webdriver_manager.chrome import ChromeDriverManager


class OneArticleAPIView(APIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    @permission_classes(AllowAny)
    def get(self, request, id, *args, **kwargs):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()
        serializer = self.serializer_class(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instance=obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes(IsAuthenticated)
    def delete(self, request, id, *args, **kwargs):
        qs = self.queryset.filter(pk=id)
        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        qs = qs.filter(user=request.user.id)
        if not qs.exists():
            return Response({"message": "You cannot delete this article"})

        obj = qs.first()
        obj.delete()

        return Response({"message": "Article is removed"}, status=status.HTTP_204_NO_CONTENT)


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument('--enable-print-browser')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# driver = webdriver.Chrome(
#     executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)


class ArticleAPIView(APIView):
    serializer_class = ArticleSerializer

    @permission_classes(AllowAny)
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        username = self.request.query_params.get('username')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        print('CATEGORY@@!', category)
        if username is not None:
            queryset = queryset.filter(user__username=username)
            if category is not None:
                queryset = queryset.filter(category__slug=category)

        if search is not None:
            print('SEARCH@@!', search)
            queryset = queryset.filter(title__icontains=search)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def upload_cloudinary(self, url, user, slug):

        response = cloudinary.uploader.explicit(url,
                                                folder=f'article/{user}/',
                                                overwrite=True,

                                                )

        url = response['url']

        print('💥', response)
        return url

    # def playwright(self, url_address):
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch()
    #         page = browser.new_page()
    #         page.goto(
    #             url_address)
    #         img = page.screenshot(path='sample.png', full_page=True)
    #         browser.close()
    #         return img

    # def screenshot(self, options={}):
    #     page_rect = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    #     base_64_png = driver.execute_cdp_cmd(
    #         "Page.captureScreenshot",
    #         {
    #             "format": "png",
    #             "captureBeyondViewport": True,
    #             "clip": {
    #                 "width": page_rect["contentSize"]["width"],
    #                 "height": page_rect["contentSize"]["height"],
    #                 "x": 0,
    #                 "y": 0,
    #                 "scale": 1
    #             }
    #         })

    #     buffer = io.BytesIO()
    #     content = base64.b64decode(base_64_png['data'])
    #     buffer.write(content)
    #     buffer.seek(0)

    #     return buffer

    # def S(self, X): return driver.execute_script(
    #     'return document.body.parentNode.scroll'+X)

    @permission_classes(IsAuthenticated)
    def post(self, request, **kwargs):
        '''
        POST /api/article/
        '''
        url_address = request.data.get('url_address')

        print('💚', request.user)

        html_text = requests.get(url_address).text
        soup = BeautifulSoup(html_text, 'lxml')
        # * og
        title = soup.find('meta', property='og:title') or None
        title = title['content'] if title != None else soup.title.string

        description = soup.find('meta', property='og:description') or None
        description = description['content'] if description != None else title
        img = soup.find('meta', property='og:image') or None
        img = img['content'] if img != None else 'No image'
        user = MyUser.objects.get(email=request.user).id

        slug = slugify(title)

        data = {
            'title': title,
            'description': description,
            'url_address': url_address,
            'image': img,
            'user': user,
            'slug': slug,
        }

        serializer = self.serializer_class(data=data)

        serializer.is_valid(raise_exception=True)

        # config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        # pdf = pdfkit.from_url(url_address, False, configuration=config)

        #! playwright
        # img = self.playwright(url_address)
        # url = self.upload_cloudinary(img, user, slug)
        # url = self.upload_cloudinary(url_address, user, slug)

        # img_url = url
        '''
        Key => articles/2/how to deploy django
        '''
        # data['file_url'] = img_url

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        article = serializer.data

        print('article 💚', article)

        return Response(article, status=res_status.HTTP_201_CREATED)


#! PAGE TO PDF
# def send_devtools(driver, cmd, params={}):
#     resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
#     url = driver.command_executor._url + resource
#     body = json.dumps({'cmd': cmd, 'params': params})
#     response = driver.command_executor._request('POST', url, body)
#     #print (response)
#     if (response.get('value') is not None):
#         return response.get('value')
#     else:
#         return None


# def save_as_pdf(driver, options={}):
#     result = send_devtools(driver, "Page.printToPDF", options)
#     if (result is not None):
#         buffer = BytesIO.BytesIO()
#         content = base64.b64decode(result['data'])
#         buffer.write(content)
#         return buffer
#     else:
#         return False


# def send_devtools(driver, cmd, params={}):
#     resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
#     url = driver.command_executor._url + resource
#     body = json.dumps({'cmd': cmd, 'params': params})
#     response = driver.command_executor._request('POST', url, body)
#     #print (response)
#     if (response.get('value') is not None):
#         return response.get('value')
#     else:
#         return None


# class ArticleUploadUrl(APIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ArticleSerializer

#     def post(self, request, **kwargs):

#         url_address = request.data.get('url_address')
#         status = request.data.get('status') or None

#         print('💚', request.user)
#         print('💚', request.data.get('url_address'))

#         html_text = requests.get(url_address).text
#         soup = BeautifulSoup(html_text, 'lxml')
#         # * og
#         title = soup.find('meta', property='og:title') or None
#         title = title['content'] if title != None else soup.title.string

#         description = soup.find('meta', property='og:description') or None
#         description = description['content'] if description != None else title
#         img = soup.find('meta', property='og:image') or None
#         img = img['content'] if img != None else 'No image'
#         user = MyUser.objects.get(email=request.user).id

#         slug = slugify(title)

#         data = {
#             'title': title,
#             'description': description,
#             'url_address': url_address,
#             'status': status,
#             'image': img,
#             'user': user,
#             'slug': slug,
#         }
#         print('💚', data)

#         serializer = self.serializer_class(data=data)
#         print('why? 💚')
#         serializer.is_valid(raise_exception=True)

#         driver = webdriver.Chrome(
#             executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
#         driver.get(url_address)
#         pdf = save_as_pdf(driver, {'landscape': False})

#         # self.driver.quit()
#         file_obj = pdf
#         file_directory_within_bucket = f'articles/{user}'
#         file_path_within_bucket = os.path.join(
#             file_directory_within_bucket,
#             title
#         )
#         media_storage = default_storage

#         media_storage.save(file_path_within_bucket, file_obj)
#         file_url = media_storage.url(file_path_within_bucket)

#         data['file_url'] = file_url
#         serializer = self.serializer_class(data=data)
#         print('why? 💚')
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         article = serializer.data
#         print(article)

#         return Response(article, status=res_status.HTTP_201_CREATED)


# class FileUploadView(APIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ArticleSerializer

#     def put(self, request, **kwargs):
#         url_address = request.data.get('url_address')
#         title = request.data.get('title')
#         user = request.user.id
#         article = Article.objects.get(pk=request.data.get('article'))

#         driver = webdriver.Chrome(
#             executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
#         driver.get(url_address)
#         pdf = save_as_pdf(driver, {'landscape': False})

#         # self.driver.quit()
#         file_obj = pdf
#         file_directory_within_bucket = f'articles/{user}'
#         file_path_within_bucket = os.path.join(
#             file_directory_within_bucket,
#             title
#         )
#         media_storage = default_storage

#         # avoid overwriting existing file

#         media_storage.save(file_path_within_bucket, file_obj)
#         file_url = media_storage.url(file_path_within_bucket)
#         data = {'file_url': file_url, 'url_address': url_address, 'user': user}

#         print('article', article)

#         serializer = self.serializer_class(instance=article, data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(instance=article)
#         print('finish!')

#         return Response(serializer.data, status=res_status.HTTP_200_OK)

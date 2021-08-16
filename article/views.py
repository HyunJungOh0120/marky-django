
import base64
import io as BytesIO
import json
import os

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import status as res_status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium import webdriver
from slugify import slugify
from user.models import MyUser

from .models import Article
from .serializers import FileUploadSerializer


def send_devtools(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    #print (response)
    if (response.get('value') is not None):
        return response.get('value')
    else:
        return None


def save_as_pdf(driver, options={}):
    result = send_devtools(driver, "Page.printToPDF", options)
    if (result is not None):
        buffer = BytesIO.BytesIO()
        content = base64.b64decode(result['data'])
        buffer.write(content)
        return buffer
    else:
        return False


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--enable-print-browser')
chrome_options.add_argument('--disable-gpu')
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


class FileUploadView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FileUploadSerializer

    driver = webdriver.Chrome(
        executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)

    def post(self, request, **kwargs):
        url_address = request.data.get('url_address')
        user = MyUser.objects.filter(pk=4).values('id')[0]['id']
        status = request.data.get('status') or None
        self.driver.get(url_address)
        pdf = save_as_pdf(self.driver, {'landscape': False})

        soup_file = self.driver.page_source
        soup = BeautifulSoup(soup_file, 'lxml')

        # * og
        title = soup.find('meta', property='og:title') or None
        description = soup.find('meta', property='og:description') or None
        img = soup.find('meta', property='og:image') or None

        self.driver.quit()
        print('💚', soup.title.string)
        print('💚', title)
        title = title['content'] if title != None else soup.title.string
        description = description['content'] if description != None else title
        url = url_address
        img = img['content'] if img != None else 'No image'
        slug = slugify(url_address)

        file_obj = pdf

        file_directory_within_bucket = f'articles/{user}'
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            title
        )

        media_storage = default_storage

        data = {
            'title': title,
            'description': description,
            'url_address': url,
            'image': img,
            'status': status,
            'user': user,
            'slug': slug
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):

            # avoid overwriting existing file

            media_storage.save(file_path_within_bucket, file_obj)
            file_url = media_storage.url(file_path_within_bucket)

            data['file_url'] = file_url if file_url else 'No file_url'

            article = Article.objects.create(
                title=title,
                description=description,
                url_address=url,
                image=img,
                status=status,
                user_id=user,
                slug=slug,
                file_url=file_url
            )

            serializer = self.serializer_class(article)

            return Response(serializer.data, status=res_status.HTTP_200_OK)
            return Response(data)

        return Response('Invalid')

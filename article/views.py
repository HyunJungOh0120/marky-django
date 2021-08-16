
import os
import io as BytesIO
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response


from django.http import JsonResponse
from selenium import webdriver
from bs4 import BeautifulSoup

from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import default_storage

import base64
import json


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
    driver = webdriver.Chrome(
        executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)

    def post(self, request, **kwargs):

        url_address = request.data.get('url_address')

        self.driver.get(url_address)
        pdf = save_as_pdf(self.driver, {'landscape': False})
        # print(json.loads(base64.b64decode(pdf['data'])))

        soup_file = self.driver.page_source
        soup = BeautifulSoup(soup_file, 'lxml')

        title = soup.find('meta', property='og:title')
        description = soup.find('meta', property='og:description')
        url = soup.find('meta', property='og:url')
        img = soup.find('meta', property='og:image')

        self.driver.quit()

        # response = Response(pdf.getvalue(), content_type='application/pdf')
        # response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        # return response

        # # organize a path for the file in bucket
        # # TODO CHANGE A TO USER ID
        file_obj = pdf
        file_directory_within_bucket = 'articles/a'

        # # synthesize a full file path; note that we included the filename
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket, title['content'])

        # file_path_within_bucket = 'articles/a/' + title['content']
        media_storage = default_storage

        media_storage.save(file_path_within_bucket, file_obj)
        file_url = media_storage.url(file_path_within_bucket)

        # # avoid overwriting existing file
        # if not media_storage.exists(file_path_within_bucket):
        #     media_storage.save(file_path_within_bucket, file_obj)
        #     file_url = media_storage.url(file_path_within_bucket)

        #     return JsonResponse({
        #         'message': 'OK',
        #         'fileUrl': file_url,
        #     })
        # else:
        #     return JsonResponse({
        #         'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
        #             filename=file_obj.name,
        #             file_directory=file_directory_within_bucket,
        #             bucket_name=media_storage.bucket_name
        #         ),
        #     }, status=400)

        info = {
            'title': title['content'],
            'description': description['content'],
            'url': url['content'],
            'img': img['content'],
            'file_url': file_url
        }

        return Response(info, status=status.HTTP_200_OK)

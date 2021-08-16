from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
import base64
from storages.backends.s3boto3 import S3Boto3Storage


class MyStorage(S3Boto3Storage):
    bucket_name = 'marky-agnes'
    location = 'media'
    file_overwrite = False


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


def save_as_pdf(driver, path, options={}):
    # https://timvdlippe.github.io/devtools-protocol/tot/Page#method-printToPDF
    result = send_devtools(driver, "Page.printToPDF", options)
    if (result is not None):
        # with open(path, 'wb') as file:
        #     file.write(base64.b64decode(result['data']))
        file_name = 'please'
        file_content = result
        MyStorage.save(file_name, file_content, file_content)

        return True
    else:
        return False


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--enable-print-browser')
chrome_options.add_argument('--disable-gpu')
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

driver = webdriver.Chrome(
    executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)

driver.get("https://romik-kelesh.medium.com/how-to-deploy-a-python-web-scraper-with-selenium-on-heroku-1459cb3ac76c")
save_as_pdf(driver, r'static', {'landscape': False})


soup_file = driver.page_source
soup = BeautifulSoup(soup_file, 'lxml')

# print(soup.head.prettify())
# name=title / description


title = soup.find('meta', property='og:title')
description = soup.find('meta', property='og:description')
url = soup.find('meta', property='og:url')
img = soup.find('meta', property='og:image')

print(title['content'] if title else "No meta title given")
print(description['content'] if description else 'No description')
print(url['content'] if url else 'No meta title given')


# print(soup.title.get_text())
# print(soup.head.meta.contents)
driver.quit()

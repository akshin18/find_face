# from selen.webdriver.common.by import By
# from selen.webdriver.support.wait import WebDriverWait
# from selen.webdriver.support import expected_conditions as Ec
# from selen import webdriver
# import time
#
#
#
#
# driver = webdriver.Opera()
#
#
# driver.get('')


import requests
import json





a = open('WhatsApp Image 2021-05-26 at 17.44.31.jpeg','rb').read()
# b = json.dumps(a)

headers = {
'content-type': 'image/jpeg',
'referer': 'https://search4faces.com/vk01/index.html',
'sec-ch-ua': '''"Chromium";v="90", "Opera";v="76", ";Not A Brand";v="99"''',
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177'
}


r = requests.post('https://search4faces.com/upload.php',headers=headers,data=a)
# print(r.text)
a = json.loads(r.text)
# print(a['url'])
print(a)
print(a['boundings'][0])


data = {'query': "vk01", 'source': "vk", 'filename': a['url'],'boundings': a['boundings'][0]}

r = requests.post('https://search4faces.com/detect.php',json=data)


print(r)
print(r.text)
ye = json.loads(r.text)
for i in ye['faces']:
    print(i)
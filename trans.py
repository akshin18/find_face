
import requests
s = requests.Session()
r = s.get('https://market.yandex.ru/catalog--mobilnye-telefony/54726/list?cpa=1&hid=91491&onstock=0&local-offers-first=0')



print(r.text)
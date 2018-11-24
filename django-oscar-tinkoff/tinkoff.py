import hashlib
import json

import requests
from django.conf import settings


class Tinkoff():
    tinkoffKey = settings.TINKOFF_KEY
    tinkoffSecrete = settings.TINKOFF_SECRET

    initURL = 'https://securepay.tinkoff.ru/v2/Init'

    def create_hash(self, newArray):
        newArray['Password'] = self.tinkoffSecrete
        sortedArray = json.loads(json.dumps(newArray, sort_keys=True))
        print(sortedArray)
        hashString = ''
        for key in sortedArray:
            value = sortedArray[key]
            hashString += str(value)

        print(hashString)

        hashString = hashlib.sha256(hashString.encode('utf-8')).hexdigest()

        return hashString

    def send_request(self, arrayData, url):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        arrayData['TerminalKey'] = self.tinkoffKey
        newArray = arrayData.copy()

        arrayData['Token'] = self.create_hash(newArray)

        response = requests.post(url, data=json.dumps(arrayData), headers=headers)
        data = response.json()

        return data

    def init_order(self, order, amount):
        data = {'OrderId': str(order.number), 'Amount': int(float(amount * 100))}
        return self.send_request(data, self.initURL)

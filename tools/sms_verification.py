import requests


class SmsVerification:

    def __init__(self, api_key, country):
        self.apiKey = api_key
        self.country = country

    def get_num(self):
        data = {'apikey': self.apiKey, 'service': 'facebook', 'country': self.country, 'form': '1'}
        r = requests.post('http://onlinesim.ru/api/getNum.php',
                          data=data)
        return r.json()

    def get_state(self, t_zid):
        r = requests.post('http://onlinesim.ru/api/getState.php?apikey={0}&tzid={1}'.format(self.apiKey, t_zid))
        return r.json()

    def set_operation_ok(self, t_zid):
        data = {'apikey': self.apiKey, 'tzid': t_zid, 'country': self.country}
        r = requests.post('http://onlinesim.ru/api/setOperationOk.php',
                          data=data)
        return r.json()
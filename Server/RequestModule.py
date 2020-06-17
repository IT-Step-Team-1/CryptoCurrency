import requests

from MainConfig import API_Settings


class API():
    get_url     = API_Settings['urls']['get_url']
    change_url  = API_Settings['urls']['change_status_url']
    headers     = {'Cache-Control': 'no-cache','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def getTransactions(self, password = API_Settings['API_password']):
        response    = requests.get(self.get_url, {'pass': password}, headers = self.headers)
        data        = response.json()

        if data['status'] == 'DONE':
            return data
        
        elif data['status'] == 'NONE':
            return 'NONE'

        else:
            return "ERROR"

        

    def ChangeStatus(self, Id, password = API_Settings['API_password']):
        response    = requests.post(self.change_url, {'pass': password, 'id': Id}, headers = self.headers)
        data        = response.json()

        if data['status'] == 'DONE':
            return data

        else:
            return 'ERROR'


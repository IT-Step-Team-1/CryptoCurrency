import requests

from Config import API_Settings


class API():
    get_url    = API_Settings['urls']['get_url']
    change_url = API_Settings['urls']['change_status_url']

    def getTransactions(self, password = API_Settings['API_password']):
        response    = requests.get(self.get_url, {'pass': password})
        data        = response.json()

        if data['status'] == 'DONE':
            return data
        
        elif data['status'] == 'NONE':
            return 'NONE'

        else:
            return "ERROR"

        

    def ChangeStatus(self, Id, password = API_Settings['API_password']):
        response    = requests.post(self.change_url, {'pass': password, 'id': Id})
        data        = response.json()

        if data['status'] == 'DONE':
            return data

        else:
            return 'ERROR'




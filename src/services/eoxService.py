import re
import json
import requests
from src.config.settings import config
from src.services.loggerService import loggerService

# disable warning fot not verified ssl
requests.packages.urllib3.disable_warnings()

class CiscoEoXApi:
    token = None

    def __init__(self):
        self.api = config['EOX_API']['URL']
        self.key = config['EOX_API']['KEY']
        self.secret = config['EOX_API']['SECRET']
        self.token = self.get_token()
        self.PageIndex = 1


    def base_connection(self, url, headers, params):
        '''
        Base connection using requests. Retrieve all pages of information.
        '''
        data = []

        while True:            
            try:
                response = requests.get(url, headers=headers, params=params, verify=False)
                loggerService.info(f'URL: {response.request.path_url}')
                if response.status_code == 200:
                    loggerService.info('Request success!')
                    data.append({"response_body": response.json(), "status_code": response.status_code})
                    self.LastIndex = response.json()['PaginationResponseRecord']['LastIndex']
                    if self.PageIndex == self.LastIndex:
                        loggerService.info('No more pages to get')
                        self.PageIndex = 1
                        break
                    loggerService.info('Get more pages')
                    self.PageIndex += 1
                    url = re.sub('EOXBy(.*?)\/[0-9]{1,5}', f'EOXBy\\1/{self.PageIndex}', url)
                else:
                    data.append({"response_body": {}, "status_code": response.status_code})
                    break
            except Exception as e:
                loggerService.error('Error trying to get data: ' + str(e))
                data.append({"response_body": {}, "status_code": 1})
                break
        return data    


    def get_token(self):
        '''
        Get a token from API and make it available for other 
        methods within the class
        '''
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        login_info = {
                'client_id': self.key,
                'client_secret': self.secret,
                'grant_type': 'client_credentials'
        }

        if self.token == None:
            try:
                response = requests.post(config['EOX_API']['OAUTH'], data=login_info, headers=headers)
                if response.status_code == 200 and 'access_token' in response.json():
                    loggerService.info('Token success!')
                    loggerService.info('Token:' + str(response.json()['access_token']))
                    return response.json()['access_token']
            except Exception as e:
                loggerService.error('Error getting token')
            return None


    def get_eox_by_dates(self, first_date, last_date):
        '''
        Gets EoX information by dates
        '''
        self.api_by_dates = self.api+'/EOXByDates'

        if self.token != None:
            headers = {
                'Authorization': 'Bearer ' + self.token
            }
            params = {
                'responseencoding': 'json'
            }
            return self.base_connection(self.api_by_dates+f'/{self.PageIndex}/{first_date}/{last_date}', headers, params)
        else:
            loggerService.error('No valid token available for query') 


    def get_eox_by_product_id(self, pid):
        '''
        Gets EoX information by product id
        '''
        self.api_by_product_id = self.api+'/EOXByProductID'  

        if self.token != None:
            headers = {
                'Authorization': 'Bearer ' + self.token
            }

            params = {
                'responseencoding': 'json'
            }

            return self.base_connection(self.api_by_product_id+f'/{self.PageIndex}/{pid}', headers, params)  
        else:
            loggerService.error('No valid token available for query') 


    def get_eox_by_sn(self, sn):
        '''
        Gets EoX information by serialnumber
        '''
        self.api_by_sn = self.api+'/EOXBySerialNumber'

        if self.token != None:
            headers = {
                'Authorization': 'Bearer ' + self.token
            }

            params = {
                'responseencoding': 'json'
            }

            return self.base_connection(self.api_by_sn+f'/{self.PageIndex}/{sn}', headers, params)    
        else:
            loggerService.error('No valid token available for query') 


    def get_eox_by_soft_rel(self, version, os=None):
        '''
        Gets EoX information by software release
        '''
        self.api_by_soft_rel = self.api+'/EOXBySWReleaseString'

        if self.token != None:
            headers = {
                'Authorization': 'Bearer ' + self.token
            }

            version_query = f'{version},{os.upper()}' if os != None else f'{version}'
 
            params = {
                'responseencoding': 'json',
                'input': version_query
            }

            return self.base_connection(self.api_by_soft_rel+f'/{self.PageIndex}', headers, params)   
        else:
            loggerService.error('No valid token available for query') 


if __name__ == '__main__':
    eoxapi = CiscoEoXApi()
    print(json.dumps(eoxapi.get_eox_by_soft_rel('IOS','12.4(15)T'), indent=4, sort_keys=True))
    #print(json.dumps(eoxapi.get_eox_by_product_id('WIC-1T='), indent=4, sort_keys=True))
    #print(json.dumps(eoxapi.get_eox_by_sn('FDO1709Y1C7'), indent=4, sort_keys=True))
    #print(json.dumps(eoxapi.get_eox_by_dates('2011-01-01', '2011-03-15'), indent=4, sort_keys=True))
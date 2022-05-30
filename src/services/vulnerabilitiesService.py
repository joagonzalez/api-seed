import json
import requests
from src.config.settings import config
from src.services.loggerService import loggerService

# disable warning fot not verified ssl
requests.packages.urllib3.disable_warnings()

class CiscoVulnApi:
    token = None

    def __init__(self):
        print(config)
        self.api = config['VULN_API']['URL']
        self.key = config['VULN_API']['KEY']
        self.secret = config['VULN_API']['SECRET']
        self.token = self.get_token()

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
                response = requests.post(config['VULN_API']['OAUTH'], data=login_info, headers=headers)
                loggerService.debug(response)
                if response.status_code == 200 and 'access_token' in response.json():
                    loggerService.debug('Token success!')
                    loggerService.debug('Token:' + str(response.json()['access_token']))
                    return response.json()['access_token']
            except Exception as e:
                loggerService.error('Error getting token')
            return None

    def all(self):
        '''
        Gets all information available from Cisco Vuln API
        '''
        if self.token != None:
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' +    self.token  
            }
            try:
                loggerService.info(self.api+'/all')
                response = requests.get(self.api+'/all', headers=headers, verify=False)
                if response.status_code == 200:
                    data = [response.json()]
                else:
                    return response.status_code
            except Exception as e:
                loggerService.error('Error trying to get data: ' + str(e))
                data = str(e)
            return data    
        else:
            loggerService.error('No valid token available for query') 

    def os(self, os, version):
        '''
        Endpoint that allows to filter by ios family version
        '''
        if self.token != None:
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' +    self.token  
            }
            try:
                loggerService.debug(self.api+'/'+os+'?version='+str(version))
                response = requests.get(self.api+'/'+os+'?version='+str(version), headers=headers, verify=False)
                if response.status_code == 200:
                    data = [response.json()]
                else:
                    return response.status_code
            except Exception as e:
                loggerService.error('Error trying to get data: ' + str(e))
                data = str(e)
            return data    
        else:
            loggerService.error('No valid token available for query')

    def latest(self, latest):
        '''
        Latest information from API
        '''
        if self.token != None:
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' +    self.token  
            }
            try:
                loggerService.debug(self.api+'/latest/'+str(latest))
                response = requests.get(self.api+'/latest/'+str(latest), headers=headers, verify=False)
                if response.status_code == 200:
                    data = [response.json()]
                else:
                    return response.status_code
            except Exception as e:
                loggerService.error('Error trying to get data: ' + str(e))
                data = str(e)
            return data    
        else:
            loggerService.error('No valid token available for query')

    def save_to_file(self, filename, data):
        '''
        Function that allows to generate a dump information
        with endpoints data
        '''
        try:
            f = open(filename, 'w')
            for line in data:
                f.write(str(line))
            f.close()
        except Exception as e:
            loggerService.error(f"Error trying to create the file {filename}")
            loggerService.error("Error: " + str(e))

    def show_advisories(self, advisories):
        '''
        Creates a clean output of advisories JSON data structure
        '''
        for advisorie in advisories['advisories']:
            print('------------------------------------')
            for key, value in advisorie.items():
                if key != 'productNames':
                    loggerService.info(key + ': ' + str(value[0:100]))
        print('------------------------------------')
        loggerService.info(f"This version has a total of {len(advisories['advisories'])} advisories...")

    def show_os_advisories(self, os, version):
        '''
        Shows in a pretty way advisories from ios images
        '''
        try:
            data = self.os(os, version)            
            self.show_advisories(data[0])
        except Exception as e:
            loggerService.error(data)

    def show_bot_advisories(self, os, version):
        '''
        Shows in a pretty way advisories from ios images
        for bot service
        '''
        try:
            data = self.os(os, version)
            i = 0
            result = '<b>Total vulnerabilities: </b>' + str(len(data[0]['advisories'])) + '\n'
            result += '-------------------- \n' 
            for advisorie in data[0]['advisories']:
                for key, value in advisorie.items():
                    if key == 'advisoryTitle' and i <= 5:
                        result += '<b>' + key + ': </b>' + value + '\n'
                        if 'sir' in advisorie:
                            result += '<b>Severity: </b>' + advisorie['sir'] + '\n'
                        if 'publicationUrl' in advisorie:
                            result += '<b>Publication Url: </b><a href="' + advisorie['publicationUrl'][8:] + '">click</a>\n'
                        if 'lastUpdated' in advisorie:
                            result += '<b>Updated: </b>' + advisorie['lastUpdated'] + '\n'
                        result += '-------------------- \n' 
                i+=1 
            return result
        except Exception as e:
            loggerService.error(data)
            return 'Empty advisory list'

if __name__ == '__main__':

    openVulApi = CiscoVulnApi()
    # loggerService.info(openVulApi.all())
    # data = openVulApi.os('ios','15.1(4)M12a')
    # openVulApi.show_advisories(data[0])
    # openVulApi.save_to_file('test', data)
    # loggerService.info(openVulApi.latest(1))
    openVulApi.show_os_advisories('ios','15.2(4)S4a')
    openVulApi.show_os_advisories('ios','15.1(4)M12a')
    openVulApi.show_os_advisories('iosxe','16.8.1')
    openVulApi.show_os_advisories('nxos','9.2(1)')
    openVulApi.show_os_advisories('aci', '11.0(2j)')
    print(openVulApi.show_bot_advisories('aci', '11.0(2j)'))
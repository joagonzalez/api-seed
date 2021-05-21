import sys
import requests
from datetime import datetime
from src.config.settings import config
from src.services.loggerService import loggerService


class Token():
    token = None
    token_time = None

    def __init__(self):
        self.key = config['INFOBLOX']['AUTH']['TOKEN']['KEY']
        self.secret = config['INFOBLOX']['AUTH']['TOKEN']['SECRET']

    def request_token(self):
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

        try:
            response = requests.post(config['INFOBLOX']['AUTH']['TOKEN']['OAUTH'], data=login_info, headers=headers)
            loggerService.info(response)
            if response.status_code == 200 and 'access_token' in response.json():
                loggerService.info('Token success!')
                loggerService.info('Token:' + str(response.json()['access_token']))
                self.token_time = datetime.now()
                loggerService.info('Token time:' + str(self.token_time))
                self.token = response.json()['access_token']
                return  self.token
        except Exception as e:
            loggerService.error('Error getting token')
        
        return None

    def is_token_expired(self):
        '''
        Method that returns boolean and check if access
        token should be refreshed
        '''
        diff = datetime.now() - self.token_time
        refresh_condition =  diff.seconds >= config['INFOBLOX']['AUTH']['TOKEN']['TOKEN_TIME']
        if refresh_condition:           
            loggerService.info('Refresh token needed! ' + str(diff.seconds) + 's since last refresh')
        
        return refresh_condition

    def get_token(self):
        if self.token is None:
            return self.request_token()

        if self.token is not None and self.is_token_expired():
            loggerService.info('Refresh token needed')
            return self.request_token()

        loggerService.info('No reason for token refresh')
        return self.token

    def get_basic_auth(self):
        '''
        Basic authentication type method returns credentials
        '''
        return [config['INFOBLOX']['AUTH']['BASIC']['USERNAME'], config['INFOBLOX']['AUTH']['BASIC']['USERNAME']]

    def get_auth_type(self):
        '''
        Returns authetication type for api
        '''
        return config['INFOBLOX']['auth_type']


tokenService = Token()
import os
os.environ['TESTING'] = 'True'


from zadarest.zadarest import ZRestClient


rest_service_url = 'https://fake.example.edu'
rest_service_token = 'fakeToken12345'

class EndpointTestCase(object):

    def setup(self):
        self.c = ZRestClient( rest_service_url, rest_service_token )



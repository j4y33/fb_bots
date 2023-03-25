import json
import boto3
import requests
from datetime import datetime
from config.config import config


class InstancesLauncher:

    def __init__(self, api_key):
        self.apiKey = api_key
        self.ec2 = boto3.resource('ec2')

    def get_avaliable_numbers(self):
        r = requests.post(
            'https://onlinesim.ru/api/getNumbersStats.php?apikey={0}&country={1}'.format(self.apiKey, config.country))

        return r.json()['services']['3223']['count']

    def get_num(self):
        data = {'apikey': self.apiKey, 'service': 'facebook', 'country': config.country, 'form': '1'}
        r = requests.post('http://onlinesim.ru/api/getNum.php',
                          data=data)
        return r.json()

    def launch_instance(self, t_zid):
        instances = self.ec2.create_instances(
            ImageId='{0}'.format(config.reg_ami),
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.small',
            KeyName='dsirf_fb_scrappers',
            SecurityGroups=['fb-scrappers'],
            UserData="{0},{1}".format(config.country, t_zid)
        )

    def launch_instances(self, instances):
        instances = self.ec2.create_instances(
            ImageId='{0}'.format(config.reg_ami),
            MinCount=1,
            MaxCount=instances,
            InstanceType='t2.small',
            KeyName='dsirf_fb_scrappers',
            SecurityGroups=['fb-scrappers'],
            UserData=config.country
        )


launch = InstancesLauncher(config.apikey)
count = launch.get_avaliable_numbers()

if count > 0:
    for i in range(count):
        t_zid = launch.get_num()
        if t_zid['response'] == 1:
            launch.launch_instance(t_zid['tzid'])
            print("Launched {0}".format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))

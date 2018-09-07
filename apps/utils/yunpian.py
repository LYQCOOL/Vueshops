# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/20 19:42'

import json

import requests


class YunPian(object):
    def __init__(self,api_key):
        self.api_key=api_key
        self.single_send_url='https://sms.yunpian.com/v2/sms/single_send.json'
    def send_sms(self,code,mobile):
        params={
            "apikey":self.api_key,
            "mobile":mobile,
            "text":"【刘勇七】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response=requests.post(self.single_send_url,data=params)
        re_dic=json.loads(response.text)
        return re_dic
        # print(re_dic)

if __name__=='__main__':
    yunpian=YunPian('d97d7caf968b3f5ec56fb2a2488140b6')
    yunpian.send_sms('2017','17738722825')


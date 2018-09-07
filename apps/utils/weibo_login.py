# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/28 18:28'


def get_auth_url():
    '''
    请求用户授权token
    :return: 
    '''
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = 'http://127.0.0.1:8000/complete/weibo/'
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=3993500018,
                                                                                            redirect_uri=redirect_uri)

    print(auth_url)


def get_access_token(code='abde2077e7000aabe40b519c9811fa30'):
    '''
    获取授权过的access token
    :param code: 
    :return: 
    '''
    access_token_url = 'https://api.weibo.com/oauth2/access_token'
    import requests
    re_dict = requests.post(access_token_url, data={
        'client_id': '3993500018',
        'client_secret': '255a336de9c48c756ea464f9339dea27',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/complete/weibo/'
    })
    pass

# b'{"access_token":"2.00bP5AOHcm_Q3E87081ccdc406btp7","remind_in":"157679999","expires_in":157679999,"uid":"6619891751","isRealName":"true"}'
def get_user_info_token(access_token,uid):
    '''
    验证是否登录获取微博用户信息
    :return: 
    '''
    user_url='https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}'.format(access_token=access_token,uid=uid)
    print(user_url)

if __name__ == "__main__":
    # get_auth_url()
    # get_access_token()
    get_user_info_token(access_token="2.00bP5AOHcm_Q3E87081ccdc406btp7", uid="6619891751")
    #获取token验证然后在应用中注册新用户或关联用户

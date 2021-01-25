#! /usr/bin/env python3
import urllib.request
import urllib.parse
import ssl
import json

# context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://192.155.1.180:8000'


# 获取token id
def token_id():
    login_url = url + '/login'
    dict = {
        'username': 'saltapi',
        'password': 'saltapi',
        'eauth': 'pam'
    }
    headers = {'Accept': 'application/json'}
    data = bytes(urllib.parse.urlencode(dict), encoding='utf-8')
    req = urllib.request.Request(url=login_url, data=data, headers=headers, method='POST')
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    tokenid = json.loads(resp)['return'][0]['token']
    return tokenid


# 远程执行
def remote_exec(tgt, fun, arg=''):
    headers = {
        'Accept': 'application/x-yaml',
        'X-Auth-Token': token_id()
    }
    dict = {
        'client': 'local',
        # 'tgt': tgt,
        # 'fun': fun
        # 'arg': arg
    }

    if tgt and fun:
        if type(tgt) == list:
            dict['expr_from'] = 'list'
            dict['tgt'] = ','.join(tgt)
        else:
            dict['tgt'] = tgt
        dict['fun'] = fun
    if arg:
        dict['arg'] = arg

    data = bytes(urllib.parse.urlencode(dict), encoding='utf-8')
    req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    return resp
    # return dict


# print(remote_exec(tgt='1',fun='2'))

# 'nginx-proxy-01,redmine'

# 执行cmd.run
print(remote_exec(tgt='saltstack-jenkins', fun='cmd.run', arg='free -m'))
#print(remote_exec(tgt=['saltstack-jenkins','redmine'],fun='cmd.run',arg='hostname'))
#print(remote_exec(tgt='saltstack-jenkins',fun='test.ping'))

# 执行state.sls
# print(remote_exec(tgt='nginx-proxy-01',fun='state.sls',arg='nginx'))
# print(remote_exec(tgt='-N webapps',fun='state.sls',arg='filebeat.webapps'))

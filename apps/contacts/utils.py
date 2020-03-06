#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 13:13
# @Author  : twosmi1e
# @Site    : 
# @File    : utils.py
# @Software: PyCharm

# encoding=utf-8
import requests
import redis

appkey = "dingsb2v8htmrjfwi4sn"
appsecret = "xEIdfFwMIlEW2qhW3sYyVwFIvoiGDrHDnrLHmeBd69lDERCulfAEgR9-YTTlHAn1"


host = "ci.redis.cnhz.shishike.com"
pwd = "!uwpXayg8yYSze2zyZpKD"
port = 6379
db = 42

def ConnectRedis():
    pool = redis.ConnectionPool(host=host, port=port, password=pwd, db=db)
    rc = redis.Redis(connection_pool=pool)
    return rc

class DingTalkInterface(object):
    def __init__(self):
        self.appkey = appkey
        self.appsecret = appsecret
        self.conn = ConnectRedis()


    def get_access_token(self):
        try:
            s = requests.session()
            response = s.get(
                "https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s" % (self.appkey, self.appsecret),
                verify=False).json()
            if response['errcode'] == 0 and "access_token" in response.keys():
                return response['access_token']
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_department_id(self):
        try:
            access_key = self.get_access_token()
            url = "https://oapi.dingtalk.com/department/list?access_token=%s&fetch_child=true&id=67424205" % access_key
            s = requests.session()
            response = s.get(url, verify=False).json()
            if response["errcode"] == 0:
                for department in response["department"]:
                    self.conn.set(department['name'], department['id'])
        except Exception as e:
            print(e)

    def get_depart_parent_id(self, department_name):
        try:
            department_id = self.conn.get(department_name)
            access_token = self.get_access_token()
            url = "https://oapi.dingtalk.com/department/list_parent_depts_by_dept?access_token=%s&id=%s" % (
                access_token, department_id.decode("utf-8"))
            print(url)
            s = requests.session()
            res = s.get(url=url, verify=False).json()
            print(res)
            if res["errcode"] == 0:
                parent_id = res['parentIds'][0]
                return parent_id
            return None
        except Exception as e:
            print(e)
            return None

    def get_user_id_by_department(self, department_id):
        try:
            access_token = self.get_access_token()
            url = "https://oapi.dingtalk.com/user/getDeptMember?access_token=%s&deptId=%s" % (
            access_token, department_id)
            s =  requests.session()
            res = s.get(url=url, verify=False).json()
            if res["errcode"] == 0:
                user_id = res['userIds']
                return user_id
            return None
        except Exception as e:
            print(e)
            return None
    def get_email_by_user_id(self,user_id):
        try:
            if user_id:
                access_token = self.get_access_token()
                url = "https://oapi.dingtalk.com/user/get?access_token=%s&userid=%s" % (
                access_token, user_id[0])
                s =  requests.session()
                res = s.get(url=url, verify=False).json()
                if res["errcode"] == 0:
                    user_id = res['email']
                    return user_id
            return None
        except Exception as e:
            print(e)
            return None



if __name__ == "__main__":
    dti = DingTalkInterface()
    print (dti.get_access_token())
    # dti.get_department_id()
    depart_id = dti.get_depart_parent_id("技术架构群")
    print(depart_id)
    user_id = dti.get_user_id_by_department(depart_id)
    print(user_id)
    user_detail = dti.get_email_by_user_id(user_id)
    print (user_detail)
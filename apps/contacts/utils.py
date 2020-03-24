#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 13:13
# @Author  : twosmi1e
# @Site    : 
# @File    : utils.py
# @Software: PyCharm

# encoding=utf-8
import requests

appkey = "dingsb2v8htmrjfwi4sn"
appsecret = "xEIdfFwMIlEW2qhW3sYyVwFIvoiGDrHDnrLHmeBd69lDERCulfAEgR9-YTTlHAn1"


class DingTalkInterface(object):
    def __init__(self):
        self.appkey = appkey
        self.appsecret = appsecret

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

    # 获取权限范围
    def get_scope(self):
        try:
            access_token = self.get_access_token()
            url = "https://oapi.dingtalk.com/auth/scopes"
            r = requests.get(url, params={'access_token':access_token})
            res = r.json()

            if res["errcode"] == 0:
                depart_id_list = res['auth_org_scopes']['authed_dept']
                return depart_id_list
        except Exception as e:
            print(e)
            return None

    # 获取子部门
    def get_sub_department(self, id):
        try:
            access_token = self.get_access_token()
            url = "https://oapi.dingtalk.com/department/list_ids"
            r = requests.get(url, params={'access_token':access_token, 'id':id})
            res = r.json()

            if res["errcode"] == 0:
                sub_dep_id_list = res["sub_dept_id_list"]
                return sub_dep_id_list
        except Exception as e:
            print(e)
            return None

    # 获取部门列表
    def get_department_list(self, id):
        try:
            access_token = self.get_access_token()
            url = "https://oapi.dingtalk.com/department/list"
            r = requests.get(url, params={'access_token': access_token, 'fetch_child': True, 'id': id})
            res = r.json()

            if res["errcode"] == 0:
                department_list = res["department"]
                return department_list
        except Exception as e:
            print(e)
            return None


    # 获取部门详情
    def get_department_detail(self, id):
        try:
            access_token = self.get_access_token()
            url = "https://oapi.dingtalk.com/department/get"
            r = requests.get(url, params={'access_token': access_token, 'id': id})
            res = r.json()

            if res["errcode"] == 0:
                return res
        except Exception as e:
            print(e)
            return None

    # 获取部门人员id列表
    def get_userid_list(self, depid):
        try:
            access_token = self.get_access_token()
            url = "https://oapi.dingtalk.com/user/getDeptMember"
            r = requests.get(url, params={'access_token': access_token, 'deptId': depid})
            res = r.json()

            if res["errcode"] == 0:
                userid_list = res["userIds"]
                return userid_list
        except Exception as e:
            print(e)
            return None

    # 获取用户详情
    def get_user_detail(self, userid):
        try:
            access_token = self.get_access_token()
            url = "https://oapi.dingtalk.com/user/get"
            r = requests.get(url, params={'access_token': access_token, 'userid': userid})
            res = r.json()

            if res["errcode"] == 0:
                return res
        except Exception as e:
            print(e)
            return None

if __name__ == "__main__":
    dti = DingTalkInterface()

    scope = dti.get_scope()


    # 所有部门名称
    # for id in scope:
    #     departments = dti.get_department_list(id)
    #     for dep in departments:
    #         print(dep["name"])
    #         if dep["name"] == "产品研发中心":
    #             cy = dep
    #
    #
    # # 获取产研全体信息
    # cy_dep_id = cy["id"]
    #
    # cy_departments = dti.get_department_list(cy_dep_id)
    # for dep in cy_departments:
    #     print(dep["name"])
    #     userid_list = dti.get_userid_list(dep["id"])
    #
    #     for id in userid_list:
    #         user_detail = dti.get_user_detail(id)
    #         print(user_detail["name"], user_detail["email"])




# coding: utf-8

"""腾讯IM聊天室
https://cloud.tencent.com/document/product/269/1520
"""

import random
import requests
import time

from lib.log import Log
from lib.im_tencent.tls_sig_api_v2 import TLSSigAPIv2
from util import add_decorator_for_public_method

KEY = ""
SDKAPPID = None
MAXNUMBER = None # 腾讯IM规定随机数最大取值范围0 - 4294967295
# 腾讯IM接口url前缀
IMGroupUrl = "https://console.tim.qq.com/v4/group_open_http_svc"
IMLoginUrl = "https://console.tim.qq.com/v4/im_open_login_svc"
IMProfileUrl = "https://console.tim.qq.com/v4/profile"

ErrorCodes = {
    10002: "服务器内部错误，请重试",
    10003: "请求命令字非法",
    10004: "参数非法，请根据错误描述检查请求是否正确",
    10005: "请求包体中携带的 Member_Account 数量超过500",
    10007: """操作权限不足，请确认该群组类型是否支持邀请加群。
            例如 AVChatRoom 和 BChatRoom 不允许任何人拉人入群""",
    10014: """群已满员，无法将请求中的用户加入群组，请尝试减少请求中 Member_Account 的数量
            或者修改该【群基础资料】的 MaxMemberNum 字段值。跳转到 群基础资料""",
    10010: "群组不存在，或者曾经存在过，但是目前已经被解散",
    10015: "群组 ID 非法，请检查群组 ID 是否填写正确",
    10016: "开发者后台通过第三方回调拒绝本次操作",
    10019: "请求的 Identifier 不存在，请检查 MemberList 中的所有 Member_Account 是否正确",
    10026: "该 SDKAppID 请求的命令字已被禁用，请联系客服",
    10037: """被邀请的成员加入群组数量超过了限制，请检查并删除群组数量超过限制的 Member_Account 
            或者按实际需要【购买升级】。跳转到 功能套餐包"""
}


def post(url, data):
    """post请求腾讯IM接口"""
    try:
        Log.info(f"{post.__doc__} 请求 {data}")
        res = requests.post(url=url, json=data)
        result = res.json()
        if result.get("ActionStatus") == "OK":
            Log.info(f"{post.__doc__} 成功 {result}")
            return result
        else:
            Log.error(f"""{post.__doc__} 失败 {result.get("ErrorInfo")} 
                {ErrorCodes.get(result.get("ErrorCode"))}""")
            return {}
    except Exception as ex:
        Log.error(f"{post.__doc__} 报错 {ex}")
        return {}


def create_im_url(root_url=IMGroupUrl, command="create_group", identifier=""):
    """生成腾讯IM请求url"""
    Log.info(f"{create_im_url.__doc__} {command}")
    sig = TLSSigAPIv2(SDKAPPID, KEY)
    usersig = sig.gen_sig(identifier)
    rand = random.randint(0, MAXNUMBER)
    return f"{root_url}/{command}?sdkappid={SDKAPPID}&identifier={identifier}&usersig={usersig}&random={rand}&contenttype=json"


add_decorator_for_public_method(staticmethod)


class IM(object):
    """腾讯im类"""

    def create_usersign(identifier="liupeng"):
        """
        生成用户签名
        :return: userSign
        """
        sig = TLSSigAPIv2(SDKAPPID, KEY)
        userSign = sig.gen_sig(identifier)
        return userSign

    def account_import(user_id: str, user_name: str, user_face_url=""):
        """
        单个帐号导入
        :param user_id: 用户中心user_id
        :param user_name: 昵称或姓名
        :param user_face_url: 头像url地址
        :return: 导入结果 bool
        """
        data = {
            "Identifier": user_id,
            "Nick": user_name,
            "FaceUrl": user_face_url
        }
        url = create_im_url(root_url=IMLoginUrl, command="account_import")
        result = post(url, data)
        # 错误码，0表示成功，非0表示失败
        code = result.get("ErrorCode", -1)
        return code == 0

    def create_group(system_user_id: str, user_id: str):
        """
        创建群组
        :param system_user_id: 系统设置用户,群主id
        :param user_id: 提问者
        :return: 会话id
        """
        _time = int(time.time())
        data = {
            # "Type": "ChatRoom",  # 群组类型：ChatRoom 聊天室（必填）
            "Type": "Public",  # 群组类型：公开群（必填）
            "GroupId": f"quicklyQA_{user_id}_{_time}",  # 用户自定义群组 ID（选填）
            "Name": f"会话_{user_id}_{_time}",  # 群名称（必填）
            "MemberList": [  # 初始群成员列表，最多500个（选填）
                {
                    "Member_Account": system_user_id,  # 成员（必填）
                }
            ]
        }
        url = create_im_url(command="create_group")
        result = post(url, data)
        return result.get("GroupId")

    def add_group_member(session_id: str, user_id: str):
        """
        增加群组成员
        :param session_id: 会话id
        :param user_id: 咨询者或咨询师的用户中心user_id
        :return: 加入结果 bool
        """
        data = {
            "GroupId": session_id,  # 要操作的群组（必填）
            "MemberList": [  # 一次最多添加500个成员
                {
                    "Member_Account": user_id  # 要添加的群成员 ID（必填）
                }]
        }
        url = create_im_url(command="add_group_member")
        result = post(url, data)
        # 加人结果：0-失败；1-成功；2-已经是群成员；3-等待被邀请者确认
        code = result.get("MemberList", [{}])[0].get("Result", 0)
        return code != 0

    def delete_group_member(session_id: str, user_id: str):
        """
        删除群组成员,不能移除群主
        :param session_id: 会话id
        :param user_id: 用户中心user_id
        :return: 加入结果 bool
        """
        data = {
            "GroupId": session_id,  # 要操作的群组（必填）
            "Silence": 1,  # 是否静默删除（选填）不在群里通知
            "MemberToDel_Account": [  # 要删除的群成员列表，最多500个
                user_id  # 群成员 ID（必填）
            ]
        }
        url = create_im_url(command="delete_group_member")
        result = post(url, data)
        # 错误码，0表示成功，非0表示失败
        code = result.get("ErrorCode", -1)
        return code == 0

    def destroy_group(session_id: str):
        """
        解散群组,不用先移除所有人,可直接解散
        :param session_id: 会话id
        :return: 解散结果 bool
        """
        data = {
            "GroupId": session_id
        }
        url = create_im_url(command="destroy_group")
        result = post(url, data)
        # 错误码，0表示成功，非0表示失败
        code = result.get("ErrorCode", -1)
        return code == 0

    def send_group_system_notification(session_id: str, message=""):
        """
        在群组中发送系统通知
        :param session_id: 会话id
        :param message: 通知内容
        :return: 通知结果 bool
        """
        data = {
            "GroupId": session_id,
            "Content": message  # 系统通知内容
        }
        url = create_im_url(command="send_group_system_notification")
        result = post(url, data)
        # 错误码，0表示成功，非0表示失败
        code = result.get("ErrorCode", -1)
        return code == 0

    def send_group_msg(session_id: str, from_user_id: str, message=""):
        """
        在群组中发送普通消息
        :param session_id: 会话id
        :param from_user_id: 指定系统设置账户发送消息
        :param message: 通知内容
        :return: 通知结果 bool
        """
        data = {
            "GroupId": session_id,
            "From_Account": from_user_id,  # 指定消息发送者（选填）
            "Random": random.randint(0, MAXNUMBER),  # 随机数字，五分钟数字相同认为是重复消息
            "MsgBody": [  # 消息体，由一个element数组组成，详见字段说明
                {
                    "MsgType": "TIMTextElem",  # 文本
                    "MsgContent": {
                        "Text": message  # 消息
                    }
                }
            ]
        }
        url = create_im_url(command="send_group_msg")
        result = post(url, data)
        # 错误码，0表示成功，非0表示失败
        code = result.get("ErrorCode", -1)
        return code == 0

    def portrait_set(im_user_id: str, tag="Tag_Profile_IM_Nick", value=""):
        """
        设置用户资料属性
        https://cloud.tencent.com/document/product/269/1500#.E6.A0.87.E9.85.8D.E8.B5.84.E6.96.99.E5.AD.97.E6.AE.B5
        :param im_user_id: 腾讯im用户id
        :param tag: 修改的字段tag, 默认修改昵称
        :param value: 修改后的值
        :return:
        """
        data = {
            "From_Account": im_user_id,
            "ProfileItem":
                [
                    {
                        "Tag": tag,
                        "Value": value
                    }
                ]
        }
        url = create_im_url(root_url=IMProfileUrl, command="portrait_set")
        result = post(url, data)
        # 错误码，0表示成功，非0表示失败
        code = result.get("ErrorCode", -1)
        return code == 0


if __name__ == "__main__":
    pass

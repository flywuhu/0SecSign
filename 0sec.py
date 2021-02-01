"""
@Time : 2021/2/1 10:35
@Author : Flywuhu
@Des : 零组文库（0sec）自动每日签到脚本
@File : 0sec.py
@IDE : PyCharm
@Motto : Another me.
"""
import requests
import re
import json
import time


class VerificationCode(object):
    def __init__(self):
        # 零组文库账号和密码
        self.User = ''
        self.Passwd = ''
        # 百度ApiKey和SecretKey
        self.ApiKey = ''
        self.SecretKey = ''
        # Server酱地址
        self.Sckey = ''
        # 通过ApiKey和SecretKey获取Access_Token
        self.Host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            self.ApiKey, self.SecretKey)
        # 获取验证码URL
        self.VerCodeUrl = 'https://wiki.0-sec.org/api/user/captchaImage'
        # 登陆URl和所需请求头
        self.LoginUrl = 'https://wiki.0-sec.org/api/user/login'
        self.LoginHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://wiki.0-sec.org',
            'Referer': 'https://wiki.0-sec.org/',
        }
        # 使用session函数保持连接
        self.s = requests.session()

    def AccessToken(self):
        # 获取百度API的AccessToken
        global AccessToken
        Response = requests.get(self.Host)
        if Response: AccessToken = Response.json()['access_token']

        return AccessToken

    def VerCode(self):
        global Uuid
        LoginResponse = self.s.get(self.VerCodeUrl)
        # 获取UUID
        Uuid = LoginResponse.json()['data']['uuid']
        # 获取登陆页面验证码连接（比较幸运的是验证码直接为base64编码，因此无需做转换）
        Img = ''.join(re.findall(r'"img":"(.*?)"', LoginResponse.text))
        # 使用AccessToken进行图片识别（调用最高精度接口，经测试该接口虽耗时最长，但识别准确率最高）
        params = {"image": Img}
        request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'  # https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic
        RequestUrl = request_url + "?access_token=" + str(self.AccessToken())
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        # 进行识别
        Res = self.s.post(RequestUrl, data=params, headers=headers).json()
        print(Res)
        # 拙比的错误处理方法
        try:
            Result = str(Res['words_result'][0]['words']).strip().replace(' ', '')
            # print(Result)
            if len(Result) == 4:
                VerCode = Result
            else:
                VerCode = 'Fuck'
        except:
            VerCode = 'Fuck'

        return VerCode

    def Account(self):
        # 登陆数据
        while True:
            c = self.VerCode()
            if not c == 'Fuck':
                Account = {
                    "account": self.User,
                    "password": self.Passwd,
                    "code": c,
                    "uuid": Uuid,
                }

                return Account

    def Login(self):
        LoginRes = self.s.post(url=self.LoginUrl, data=json.dumps(self.Account()), headers=self.LoginHeaders)

        return LoginRes.text

    def Sign(self):
        while True:
            a = json.loads(self.Login())
            if a['success'] == True:
                ZeroToken = a['data']['token']
                self.SignHeaders = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Accept-Encoding': 'gzip, deflate',
                    'Zero-Token': '{}'.format(ZeroToken),
                    'Origin': 'https://wiki.0-sec.org',
                    'Connection': 'close',
                    'Referer': 'https://wiki.0-sec.org/',
                    'Cookie': 'Zero-Token={}'.format(ZeroToken),
                }
                SignURL = 'https://wiki.0-sec.org/api/front/user/sign'
                SignRes = self.s.post(url=SignURL, headers=self.SignHeaders).text

                return SignRes

    # Server酱推送
    def server_send(self):
        if '操作成功' in self.Sign():
            DateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            Profile = json.loads(self.s.get(url='https://wiki.0-sec.org/api/profile',headers=self.SignHeaders).text)['data']['credit']
            msg = "[+] 今日零组文库签到完成，详细积分请登陆查看~ " + "\n- 当前积分是: " + str(Profile) + "\n- 现在时间是: " + str(DateTime)
            server_url = self.Sckey
            data = {
                'text': "零组文库签到完成~",
                'desp': msg
            }
            requests.post(server_url, data=data)
            print(data)

    def main(self):
        self.server_send()


# 云函数入口
def main_handler(event, context):
    run = VerificationCode()
    a = run.main()


if __name__ == '__main__':
    run = VerificationCode()
    b = run.main()


import random
import time


class MyChat:
    def __init__(self, itchat):
        '''初始化'''
        self.itchat = itchat
        self.friends = itchat.get_friends(update=True)[600:]
        self.total = len(self.friends)
        self.myname = self.friends[0]['UserName']
        self.mass_send_setting()
        # 机器人设置
        self.robot_setting()
        # 人脸识别设置
        self.aip_setting()

    def mass_send_setting(self):
        # 群发设置1为打开群发,0 为关闭群发
        self.mass_setting = 1
        # 每次发送数量
        self.send_friends_count = 50
        # 每次群发间隔
        self.send_time = random.randint(5, 10)
        # 每轮群发间隔时间
        self.mass_time_interval = random.randint(30, 120)
        # 默认祝福信息
        self.blessing_string()

    def robot_setting(self):
        self.redio = 0
        self.key = '8edce3ce905a4c1dbb965e6b35c3834d'
        self.api_url = 'http://www.tuling123.com/openapi/api'

    def aip_setting(self):
        self.app_id = '11504536'
        self.api_key = 'pEctKjYg9CKVY9Qn6x1woTnv'
        self.secret_key = 'oA4Hw81cjWVDxxWxusxCX80KxkmuoUqY'

    def robot(self, msg, requests):
        data = {
            'key': self.key,
            'info': msg,
            'userid': 'wechat-robot',
        }
        try:
            r = requests.post(self.api_url, data=data).json()
            return r.get('text')
        except:
            return

    def blessing_string(self):
        blessing_string = '''我是贷@#@款公司的小童,这是我的新号码:18909339534 / 15293698584 , 有资金的需求可以联系我,谢谢!'''
        return blessing_string

    def send_start(self, start, end, send_msg, times):
        print('第{0}轮群发开始...'.format(times + 1))
        for friend in self.friends[start: end]:
            self.itchat.send(send_msg.format(friend_name=friend['DisplayName'] or friend['NickName']),
                             friend['UserName'])
            print(friend['NickName'])
            print(send_msg)
            time.sleep(self.send_time)
        print('第{0}轮群发结束,下次群发还有{1}秒'.format(times + 1, self.mass_time_interval))
        time.sleep(self.mass_time_interval)

    def mass_send(self, send_msg):
        '''这里是循环发送'''
        times = 0
        while times < int(self.total / self.send_friends_count):
            start = times * self.send_friends_count
            end = (1 + times) * self.send_friends_count
            self.send_start(start, end, send_msg, times)
            times += 1
        else:
            print('所有群发已经结束!')

    def mass(self, bless_msg):
        '''群发主函数'''
        if bless_msg == '':
            bless_msg = self.blessing_string()
        if self.mass_setting:
            prefix_msg = '{friend_name},您好!'
            send_msg = prefix_msg + bless_msg
            self.mass_send(send_msg)

    def friend_count(self):
        '''微信好友数量'''
        male = female = other = 0
        for i in self.friends:
            sex = i['Sex']
            if sex == 1:
                male += 1
            elif sex == 2:
                female += 1
            else:
                other += 1
        self.friend_info_output(male, female, other)

    def friend_info_output(self, male, female, other):
        '''微信好像数量统计输出'''
        string = '\t\n你的微信总的用户数量为{total},' \
                 '\t\n其中女性用户的比例为{female:.2%},' \
                 '\t\n男性用户的比例为{male:.2%},' \
                 '\t\n人妖的比例为{other:.2%}\n'
        print(string.format(
            total=self.total,
            female=female / self.total,
            male=male / self.total,
            other=other / self.total
        ))

    '''
    以下为用户发送返回函数
    '''

    def Text(self, msg):
        # 发送一条提示给文件助手
        self.itchat.send_msg(
            '[{time}]收到好友@{friend} 的消息: {info}'.format(
                time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['CreateTime'])),
                friend=msg['User']['NickName'],
                info=msg['Text']
            ),
            'filehelper'
        )
        # 回复给好友
        return '[自动回复]您好，我现在有事不在，一会再和您联系。\n已经收到您的的信息：{info}\n'.format(
            info=msg['Text']
        )

    '''
    人脸识别模块
    '''

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def aip_find(self, client, phtoImage):
        format_string = '颜值{best},专家给你评分{score}.'
        image = self.get_file_content(phtoImage)
        r = client.detect(image, options={
            'face_files': 'age,gender,beauty,qualities'
        })
        for i in r['result']:
            score = i['beauty']
            if score >= 90:
                result = '优秀'
            elif score >= 80:
                result = '良好'
            elif score >= 70:
                result = '中等'
            elif score >= 60:
                result = '及格'
            else:
                result = '不及格'
            print(format_string.format(result, score))

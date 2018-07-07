import itchat, time
from itchat.content import *
from public import MyChat
import requests
from aip import AipFace


# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True,
                     isGroupChat=True, isMpChat=True)
def text_reply(msg):
    if public.redio:
        default_replay = 'I received: {}'.format(msg['Text'])
        replay = public.robot(msg, requests)
        return replay or default_replay
    # 当消息不是由自己发出的时候
    elif msg['FromUserName'] == myUserName:
        '''通过微信控制群发信息'''
        pass
    elif msg['Type'] == 'Text' and not msg['FromUserName'] == myUserName:
        '''自动回复信息'''
        public.Text(msg)
    elif (msg['Type'] == 'Attachment'
          or msg['Type'] == 'Video'
          or msg['Type'] == 'Recording'):

        msg_content = msg['FileName']
        msg['Text'](str(msg_content))
    elif msg['Type'] == 'Map':
        pass
    elif msg['Type'] == 'Picture':
        print(msg)
    else:
        pass


def main(public):
    public.friend_count()
    bless_msg = input(
        '请输入祝福信息,如果不输入任何信息发送默认祝福信息:{default_bless_msg} :'.format(
            default_bless_msg=public.blessing_string()
        )
    )
    confirm_send = 0
    try:
        confirm_send = int(input('确认发送? [1 为发送 0 为取消]'))
    except Exception as e:
        print(e)
    if confirm_send:
        public.mass(bless_msg)


if __name__ == '__main__':
    itchat.auto_login(True)
    # 实例化public模块
    public = MyChat(itchat)
    # 人脸识别
    client = AipFace(public.app_id, public.app_id, public.secret_key)
    # 取出用户名称
    myUserName = public.myname
    # 主函数
    main(public)
    itchat.run()

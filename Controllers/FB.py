from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from config import auth, cache, FB_TOKEN
from Models.FBSendModel import *
import requests
import json

parser = reqparse.RequestParser()
parser.add_argument('access_token')
parser.add_argument('hub.verify_token')
parser.add_argument('hub.challenge')
parser.add_argument('entry', type=list, location='json')

class FBWebhook(Resource):
    def get(self):
        args = parser.parse_args()
        token = args['hub.verify_token'] if 'hub.verify_token' in args else None
        if FB_TOKEN == token:
            challenge = args['hub.challenge'] if 'hub.challenge' in args else None
            return int(challenge), 200
        return 'Hello World!', 200
 
    def post(self):
        try:
            args = parser.parse_args()
            message_entries = args['entry'] if 'entry' in args else None
            for entry in message_entries:
                if entry.get('messaging'):
                    messagings = entry['messaging']
                    for message in messagings:
                        sender = message['sender']['id']
                        if message.get('message'):
                            text = message['message']['text']
                            return self.sendToSender(sender, text)
                elif entry.get('changes'):
                    changes = entry['changes']
                    for change in changes:
                        value = change['value']
                        comment = None
                        if value.get('post_id'):
                            comment = value['comment_id']
                        elif value.get('comment_id'):
                            comment = value['comment_id']
                        if comment is not None and value.get('message'):
                            text = value['message']
                            print("{} says {}".format(comment, text))
                            return self.replyToComment(comment, text)
            return {
                'isSuccess': False,
                'message': 'there is no message received'
            }
        except BaseException as e:
            print('BaseException', e)
            return {
                'isSuccess': False,
                'message': e.args
            }
    def botMessage(self, text=""):
        message = text
        if text == "hello":
            message = "Hello, 這裡是東森購物小幫手, 請問有什麼可以為您服務的嗎?"
        elif text == "info" or text == "help" or text == "support":
            message = "東森購物小幫手提供即時線上客服的服務，若有需要真人語音服務，請撥打24小時免費客服專線0800-057-999。"
        elif text == "menu":
            message = "若有任何購物的需求，請連結至東森購物官方網站https://www.etmall.com.tw/選購。"
        elif text == "+1":
            message = "感謝您的下單選購，請到我們的賣場完成此商品結帳流程:https://ehs-shop.herokuapp.com/detail/2"
        else:
            message = "無法辨識您的留言訊息。歡迎到此選購我們的特殊商品:https://ehs-shop.herokuapp.com/"
        return message

    def sendToSender(self, sender, sending_text):
        try:
            post_message_url = 'https://graph.facebook.com/v4.0/me/messages?access_token={token}'.format(token=FB_TOKEN)
            to = sender
            message = self.botMessage(sending_text.lower())
            response_message = json.dumps({"messaging_type": "RESPONSE",
                                        "recipient":{"id": str(to)}, 
                                        "message":{"text":message}})
            req = requests.post(post_message_url,
                    headers={"Content-Type": "application/json"}, 
                    data=response_message)
            print("[{}] Reply to {}: {}", req.status_code, to, message)
            return {'isSuccess': True, 'message': "Message sent successfully!"}
        except BaseException as e:
            print('BaseException', e)
            return {
                'isSuccess': False,
                'message': e.args
            }

    def replyToComment(self,comment, text):
        try:
            message = self.botMessage(text)
            post_message_url = 'https://graph.facebook.com/v4.0/{comment}/private_replies?access_token={token}&message={message}'.format(comment=comment, token=FB_TOKEN, message=message)
            req = requests.post(post_message_url)
            print("[{}] Reply to {}: {}", req.status_code, comment, message)
            return {'isSuccess': True, 'message': "Message sent successfully!"}
        except BaseException as e:
            print('BaseException', e)
            return {
                'isSuccess': False,
                'message': e.args
            }

class FBLiveComment(Resource):
    decorators = [auth.login_required]
    def get(self):
        try:
            args = parser.parse_args()
            token = args['access_token'] if 'access_token' in args else None
            if token is not None:
                s = requests.session()
                url = 'https://graph.facebook.com/v4.0/me/live_videos?status=LIVE_NOW&access_token='+token
                response = s.get(url)
                html = json.loads(response.text)
                id = html['data'][0]['id']

                comment_url = 'https://graph.facebook.com/v4.0/'+id+'/comments?access_token='+token
                comment_response = s.get(comment_url)
                comment_html = json.loads(comment_response.text)
                comment = comment_html['data'][-1]['message']
                user_id = comment_html['data'][-1]['from']['id']
                if comment.find('+1') >=0:
                    redirectLink = "https://ehs-shop.herokuapp.com/detail/2"
                    try:
                        fb = FBSendModel(user_id, redirectLink, comment)
                        fb.save_to_db()
                        return {'isSuccess': True, 'message': comment, 'user_id':user_id, 'redirect':redirectLink}
                    except BaseException as e:
                        return {
                            'isSuccess': False,
                            'message': e.args
                        }
                else:
                    return {'isSuccess': False, 'message': 'there is no any plus 1 message'}
            else:
                return {'isSuccess': False, 'message': 'there is no token assigned'}
        except BaseException as e:
            return {
                'isSuccess': False,
                'message': e.args
            }

class FBSendToChat(Resource):
    decorators = [auth.login_required]
    def get(self):
        try:
            post_message_url = 'https://graph.facebook.com/v4.0/me/messages?access_token={token}'.format(token=FB_TOKEN)
            messagesObj = FBSendModel.query.filter_by(is_sent=False).order_by(FBSendModel.userId).all()
            if messagesObj is not None:
                for messageObj in messagesObj:
                    messageData = messageObj.data
                    to = messageData['userId']
                    message = messageData['pageLink']
                    response_message = json.dumps({"messaging_type": "RESPONSE",
                                                "recipient":{"id": str(to)}, 
                                                "message":{"text":message}})
                    req = requests.post(post_message_url,
                            headers={"Content-Type": "application/json"}, 
                            data=response_message)
                    if req.status_code == 200:
                        FBSendModel.query.filter_by(userId=to).update({'is_sent': True})
                    print("[{}] Reply to {}: {}", req.status_code, to, message)
                return {'isSuccess': True, 'message': "Message sent successfully!"}
            else:
                return {'isSuccess': False, 'message': 'there is no token assigned'}
        except BaseException as e:
            print('BaseException', e)
            return {
                'isSuccess': False,
                'message': e.args
            }
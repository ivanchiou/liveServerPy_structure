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

def sendTextToSender(to, message):
    try:
        post_message_url = 'https://graph.facebook.com/v4.0/me/messages?access_token={token}'.format(token=FB_TOKEN)
        response_message = json.dumps({"messaging_type": "RESPONSE",
                                    "recipient":{"id": str(to)}, 
                                    "message":{"text":message}})
        req = requests.post(post_message_url,
                headers={"Content-Type": "application/json"}, 
                data=response_message)
        if req.status_code == 200:
            FBSendModel.query.filter_by(userId=to).update({'is_sent': True})
            return {'isSuccess': True, 'message': "Message sent successfully!"}
        return {'isSuccess': False, 'message': "Message sent failed!"}
    except BaseException as e:
        return {
            'isSuccess': False,
            'message': e.args
        }

class FBWebhook(Resource):
    def get(self):
        args = parser.parse_args()
        token = args['hub.verify_token'] if 'hub.verify_token' in args else None
        if FB_TOKEN == token:
            challenge = args['hub.challenge'] if 'hub.challenge' in args else None
            return int(challenge), 200
        return 'Hello World!', 200
 
    #接收用戶透過messager傳來的訊息
    def post(self):
        try:
            args = parser.parse_args()
            message_entries = args['entry'] if 'entry' in args else None
            for entry in message_entries:
                messagings = entry['messaging']
                for message in messagings:
                    sender = message['sender']['id']
                    if message.get('message'):
                        text = message['message']['text']
                        return sendTextToSender(sender, text)
            return {
                'isSuccess': False,
                'message': 'there is no message received'
            }
        except BaseException as e:
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
            if messagesObj is not None and len(messagesObj)>0:
                for messageObj in messagesObj:
                    messageData = messageObj.data
                    to = messageData['userId']
                    message = messageData['pageLink']
                    sendTextToSender(to,message)
                return {'isSuccess': True, 'message': "Message sent successfully!"}
            else:
                return {'isSuccess': False, 'message': 'there is no user comment'}
        except BaseException as e:
            return {
                'isSuccess': False,
                'message': e.args
            }
import requests
import json

slack_channel = '#jetson-camera'
slack_icon_url = 'https://i.pinimg.com/originals/fa/2e/58/fa2e583668a7d0ec15f4fa1bcb20975d.jpg'
slack_user_name = 'Jetson Cam'

def post_message_to_slack(text, args, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': args.slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_url': slack_icon_url,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()

def post_file_to_slack(
  text, args, file_name, file_bytes, file_type=None, title=None
):
    return requests.post(
      'https://slack.com/api/files.upload', 
      {
        'token': args.slack_token,
        'filename': file_name,
        'channels': slack_channel,
        'filetype': file_type,
        'initial_comment': text,
        'title': title
      },
      files = { 'file': file_bytes }).json()
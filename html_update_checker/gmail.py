import pickle
import base64
from functools import partial
from email.mime.text import MIMEText

from googleapiclient.discovery import build

#############
#   Example #
#############

# To keep it simple, the complete authorization process is removed. Only the pickled token file remains and is loaded.
# Furthermore, with the use of partial, the function send_message parameters are reduced to only receive the message.

# 1. step: Create message
# message = create_message("<sender mail>", "<to mail>", "<subject>", "<Body as HTML>")

# 2. step: Send message 
# send_message(message)

#####################
# Implementation    #
#####################

def create_message(sender, to, subject, message_text):
    """Create a message for an email.
      Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
      Returns:
          An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, user_id, message):
    """Send an email message.
      Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.
      Returns:
          Sent Message.
    """
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    return message


def get_service(path):
    with open(rf'{path}', 'rb') as token:
        creds = pickle.load(token)
    service = build('gmail', 'v1', credentials=creds)
    return service

send_message = partial(send_message, get_service(r"token.pickle"), "me")

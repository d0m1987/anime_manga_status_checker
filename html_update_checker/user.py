from typing import Union, List
from collections import defaultdict

from html_update_checker.homepage import HomepageUpdateInterface

class User(HomepageUpdateInterface):
    def __init__(self, email:str):
        self.email = email
        self.homepages = dict()
        self.pending_update_notifications = defaultdict(list)
    
    def add_homepage_notifications(self, homepage:Union["Homepage", List["Homepage"]]):
        pass

    def remove_homepage_notifications(self, homepage:Union["Homepage", List["Homepage"]]):
        pass
    
    def send_updates(self):
        pass

    def add_update_notification(homepage:"Homepage", episode:"Episode"):
        pass


    
        


from datetime import datetime
from json import JSONEncoder

from db_manager import insert_notification, get_notifications

class Notification():
    def __init__(self, name:str, type:str, description:str, id:int =-1, date:datetime =datetime.now(), is_read:bool =False) -> None:
        self.name = name
        self.type = type
        self.description = description
        self.date = date
        self.is_read = is_read
        if id == -1:
            self.id = insert_notification(self.name, self.type, self.description, self.date, self.is_read)
        else:
            self.id = id

    @classmethod
    def get_all(cls):
        notifications = {}
        list_rows = get_notifications()
        
        if list_rows:
            for rows in list_rows:
                notification = Notification(name=rows[1],type=rows[2],description=rows[3],id=rows[0], date=rows[4], is_read=rows[5])
                notifications[notification.id] = notification

        return notifications 
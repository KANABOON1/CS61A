class MinList:
    def __init__(self):
        self.items=[]
        self.size=0
    def append(self,item):
        self.items.append(item)
        self.size+=1
    def pop(self):
        self.size-=1
        min_num,min_index=self.items[0],0
        for i in range(len(self.items)):
            if self.items[i]<min_num:
                min_num, min_index = self.items[i], i
        return self.items.pop(min_index)

class Email:
    def __init__(self,msg,sender_name,recipient_name):
        self.message=msg
        self.sender_name=sender_name
        self.recipient_name=recipient_name
class Server:
    def __init__(self):
        self.client={}
    def send(self,email):


    def register_client(self,client,client_name):
        if client_name in self.client:
            self.client[client_name].append(client)
        else:
            self.client[client_name]=[client]


class Client:
    def __init__(self,server,name):
        self.inbox=[]
        self.name=name
        self.server=server

    def compose(self,msg,recipientz_name):


    def receive(self,email):

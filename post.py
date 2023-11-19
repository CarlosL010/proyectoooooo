from usuario import User
class Post:
    
    def __init__(self,username,multimedia,tags,caption,date,publisher):
        
        self.username=username
        self.multimedia=multimedia
        self.tags=tags
        self.caption=caption
        self.date=date
        self.publisher=publisher
        self.likes=[]
        self.comments=[]

    def show(self):
        return(self.username,self.multimedia,self.tags,self.caption,self.date)
    

class User:

    

    def __init__(self,firstName,lastName,email,username,id,following,):
        
        self.firstName=firstName
        self.lastName=lastName
        self.email=email
        self.username=username
        self.id=id
        self.followings=following
        
        
        
        self.publication=[]
        

    def show(self):
        return(self.firstName,self.lastName,self.email,self.username,self.id,self.followings)
    
    def get_id(self):
     return self.id
    
    

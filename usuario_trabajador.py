from usuario import User

class UserTrabajador(User):
    def __init__(self, firstName, lastName, email, username,id,following, department):
        super().__init__(firstName, lastName, email, username,id,following)
        self.department = department
        self.likes=[]
        self.publication=[]
        
        

    def show(self):
        user_info = super().show()
        return user_info + (self.department) + (self.likes) 
    
    def get_id(self):
     return self.id
    
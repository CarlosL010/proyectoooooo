from usuario import User

class UserEstudiante(User):
    def __init__(self, firstName, lastName, email, username,id,following, major):
        super().__init__(firstName, lastName, email, username,id,following)
        self.major = major
        self.likes=[]
        self.publications=[]
        

    def show(self):
        user_info = super().show()
        return user_info + (self.major) + (self.likes) 
    
    def get_id(self):
     return self.id
     
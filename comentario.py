
import datetime


class Comentario:

    
    def __init__(self, user, post, texto):
        self.user = user
        self.post = post
        self.texto = texto
        self.fecha = datetime.datetime.now()

    
    def show(self):
        print(f"{self.user.username} comentó: {self.texto} ({self.fecha})")

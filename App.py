import requests
import json
from usuario import User
from post import Post
from usuario_estudiante import UserEstudiante
from usuario_trabajador import UserTrabajador
from comentario import Comentario
import datetime
import random

class App():

    def __init__(self):
        self.usuarios_registrados = []
        users = self.get_user()
        self.post_publicados=[]
        self.posts=self.get_post()
        self.followings=[]

    def get_user(self):
        # Realiza una solicitud GET a la API que proporciona información de usuarios
        response = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json")
        
        # Convierte la respuesta en formato JSON a un diccionario de Python
        data = json.loads(response.text)
        
        # Itera a través de los datos de usuario obtenidos de la API
        for user_data in data:
            # Verifica si el usuario tiene el campo 'career', indicando que es un estudiante
            if 'major' in user_data:
                # Crea una instancia de la clase UserEstudiante para el estudiante
                user = UserEstudiante(user_data['firstName'], user_data['lastName'], user_data['email'], user_data['username'],user_data["id"], user_data["following"],  user_data['major'])
            else:
                # Crea una instancia de la clase UserTrabajador para el trabajador
                user = UserTrabajador(user_data['firstName'], user_data['lastName'], user_data['email'], user_data['username'],user_data["id"], user_data["following"], user_data['department'])
            
            # Agrega el usuario creado a la lista de usuarios registrados en la aplicación
            self.usuarios_registrados.append(user)

        # Retorna la lista de usuarios registrados
        return self.usuarios_registrados
    

    def get_post(self):
        # Realiza una solicitud GET a la API que proporciona información de los posts
        response = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json")
        
        # Convierte la respuesta en formato JSON a un diccionario de Python
        data = json.loads(response.text)
        
        # Itera a través de los datos de posts obtenidos de la API
        for post_data in data:
            # Crea una instancia de la clase post 
            post=Post(post_data["type"],post_data["caption"],post_data["date"],post_data["tags"],post_data["multimedia"],post_data["publisher"])
        #agrega el post creado a la lista de post publicados
            self.post_publicados.append(post)

        return self.post_publicados
        

    #GESTION DE PERFIL 

    #Funciona 
    def register_user(self):
        
        while True:
           # Solicita el nombre del usuario
          firstName = input("Ingrese su nombre: ")
           # Solicita el apellido del usuario
          lastName = input("Ingrese su apellido: ")
           # Solicita el correo electrónico del usuario y valida que pertenezca a la universidad
          email = input("Ingrese su correo electrónico: ")
          if email.endswith("@correo.unimet.edu.ve"):
              break
          else:
              print("El email debe terminar en @correo.unimet.edu.ve, intente de nuevo")
            
        
        # Solicita el nombre de usuario del usuario
        username = input("Ingrese su nombre de usuario: ")
        # Solicita el tipo de usuario (estudiante o trabajador)
        while True:
            user_type = input("Ingrese su tipo de usuario (estudiante o trabajador): ")
            # Verifica si el usuario ingresó una opción válida
            if user_type.lower() in ["estudiante", "trabajador"]:
                # Sale del bucle
                break
            else:
                # Imprime un mensaje de error
                print("Dato inválido, intente de nuevo")
        
        # Verifica si el usuario ingresó 'estudiante' como tipo de usuario
        if user_type.lower() == 'estudiante':
            # Solicita la carrera del estudiante
            major = input("Ingrese su carrera: ")
            # Genera un id aleatorio para el usuario
            id=random.randint(1,1000)

            followings=[id]
            
            # Crea una instancia de la clase UserEstudiante para el estudiante
            user = UserEstudiante(firstName, lastName, email, username,id,followings, major)
        elif user_type.lower()=="trabajador":
            # Solicita el departamento del trabajador
            department = input("Ingrese su departamento: ")
            #genera un id aleatorio para el usuario
            id=random.randint(1,1000)

        
            

            followings=[id]

            # Crea una instancia de la clase UserTrabajador para el trabajador
            user = UserTrabajador(firstName, lastName, email, username,id, followings, department)

        
        
        # Agrega el usuario creado a la lista de usuarios registrados en la aplicación
        self.usuarios_registrados.append(user)
        # Imprime los datos del registro dependiendo del tipo de usuario que sea 
        if isinstance(user,UserEstudiante):
         print(f"""El usuario se ha registrado con los siguientes datos: 
               Nombre:   {user.firstName}
               Apellido: {user.lastName}
               email:    {user.email}
    Nombre de Usuario:   {user.username}
                     id: {user.id}
               Carrera:  {user.major} """)

        else:
            print(f"""El usuario se ha registrado con los siguientes datos: 
               Nombre:   {user.firstName}
               Apellido: {user.lastName}
               email:    {user.email}
    Nombre de Usuario:   {user.username}
                    id:  {user.id}
               Carrera:  {user.department} """)
            

        # Abre el archivo de texto en modo escritura
        archivo = open("datos_registro.txt", "w")
        # Itera sobre la lista de usuarios registrados
        for user in self.usuarios_registrados:
            # Escribe los datos de cada usuario en el archivo, separados por "="
            archivo.write(user.firstName + "=" + user.lastName + "=" + user.email + "=" + user.username + "=" + str(user.id))
            # Verifica si el usuario es estudiante o trabajador
            if isinstance(user, UserEstudiante):
                # Escribe la carrera del usuario
                archivo.write(user.major + "\n")
            else:
                # Escribe el departamento del usuario
                archivo.write(user.department + "\n")
        # Cierra el archivo
        archivo.close()

        
        # Retorna el usuario creado
        return user
    
    


    





    
    #Funciona pero falta agregar la lista de publicaciones
    
    def search_user(self):
        
     users_found = []
     # Crea una variable booleana para indicar si se encontró algún usuario
     found = False
    
    # Pide al usuario que elija un filtro entre username, major o department
     filter = input("Ingrese el filtro que desea usar (username, major o department): ")

     
    
    # Pide al usuario que ingrese el valor que desea buscar
     value = input("Ingrese el username de la persona,la carrera o el departamento que desea buscar: ")
    
    # Itera a través de la lista de usuarios registrados en la aplicación
     for user in self.usuarios_registrados:
        # Verifica si el filtro es 'username'
        if filter.lower() == 'username':
            # Compara el valor del filtro con el atributo 'username' del usuario
            if value.lower() == user.username.lower():
                # Agrega el usuario a la lista de usuarios encontrados
                users_found.append(user)
                # Cambia el valor de la variable booleana a verdadero
                found = True
                #Itera sobre la lista para imprimir los datos
                for users in users_found:
                     print(f"""   USUARIO ENCONTRADO
                                 -----------------------------                             
                                  Nombre: {users.firstName}
                  
                                  Username: {users.username} """)
                     
                     
                print("Publicaciones:")
                


            
               
               
                     
        # Verifica si el filtro es 'major'
        elif filter.lower() == 'major':
            # Verifica si el usuario es una instancia de la clase UserEstudiante
            if isinstance(user, UserEstudiante):
                # Compara el valor del filtro con el atributo 'major' del usuario
                if value.lower() == user.major.lower():
                    # Agrega el usuario a la lista de usuarios encontrados
                    users_found.append(user)
                    # Cambia el valor de la variable booleana a verdadero
                    found = True
                    #Itera sobre la lista para imprimir los datos 
                    for users in users_found:
                     print(f"""   USUARIO ENCONTRADO
                                 -----------------------------                             
                                  Nombre: {users.firstName}
                                  Username: {users.username} """)
                     
                    print("Publicaciones:  ")
                    
                
                



        # Verifica si el filtro es 'department'
        elif filter.lower() == 'department':
            # Verifica si el usuario es una instancia de la clase UserTrabajador
            if isinstance(user, UserTrabajador):
                # Compara el valor del filtro con el atributo 'department' del usuario
                if value.lower() == user.department.lower():
                    # Agrega el usuario a la lista de usuarios encontrados
                    users_found.append(user)
                    # Cambia el valor de la variable booleana a verdadero
                    found = True
                    #Itera sobre la propia lista para imprimir los datos 
                    for users in users_found:
                     print(f"""   USUARIO ENCONTRADO
                                 -----------------------------                             
                                  Nombre: {users.firstName}
                                  Username: {users.username} """)
                     
                    print("Publicaciones:  ")

                

                
                   
     # Verifica si la variable booleana es falsa
     if not found:
         # Imprime el mensaje de error correspondiente al filtro usado
         if filter.lower() == 'username':
             print("No existen usuarios registrados con ese username")
         elif filter.lower() == 'major':
             print("No existen usuarios registrados de esa carrera")
         elif filter.lower() == 'department':
             print("No hay existen usuarios registrados de ese departamento")


    

    #funciona 
    def modify_user(self):
       # Pide al usuario que ingrese el nombre de usuario del usuario que quiere modificar
       username = input("Ingrese el nombre de usuario del usuario que quiere modificar: ")
       
       try:
        # Busca al usuario que tiene el nombre de usuario ingresado
        user = next(user for user in self.usuarios_registrados if user.username == username)
        # Muestra los datos actuales del usuario
        print("Los datos actuales del usuario son:")
        print(f"Nombre: {user.firstName}")
        print(f"Apellido: {user.lastName}")
        print(f"Correo: {user.email}")
        # Verifica si el usuario es estudiante o trabajador
        if isinstance(user, UserEstudiante):
            print(f"Carrera: {user.major}")
        else:
            print(f"Departamento: {user.department}")
        print()
        
        # Pide al usuario que elija qué dato quiere modificar
        option = input("Ingrese qué dato quiere modificar (nombre, apellido, correo, carrera o departamento): ")
        
        # Verifica si el usuario quiere modificar el nombre
        if option.lower() == 'nombre':
            # Pide al usuario que ingrese el nuevo nombre
            new_name = input("Ingrese el nuevo nombre: ")
            # Actualiza el atributo 'firstName' del usuario
            user.firstName = new_name
            # Muestra un mensaje de confirmación
            print("El nombre del usuario ha sido modificado exitosamente.")
        
        # Verifica si el usuario quiere modificar el apellido
        elif option.lower() == 'apellido':
            # Pide al usuario que ingrese el nuevo apellido
            new_last_name = input("Ingrese el nuevo apellido: ")
            # Actualiza el atributo 'lastName' del usuario
            user.lastName = new_last_name
            # Muestra un mensaje de confirmación
            print("El apellido del usuario ha sido modificado exitosamente.")
        
        # Verifica si el usuario quiere modificar el correo
        elif option.lower() == 'correo':
            # Pide al usuario que ingrese el nuevo correo
            new_mail = input("Ingrese el nuevo correo: ")
            # Valida que el nuevo correo pertenezca a la universidad
            if not new_mail.endswith("@correo.unimet.edu.ve"):
                print("Correo invalido, intente de nuevo")
                return new_mail
            # Actualiza el atributo 'email' del usuario
            user.email = new_mail
            # Muestra un mensaje de confirmación
            print("El correo del usuario ha sido modificado exitosamente.")
        
        # Verifica si el usuario quiere modificar la carrera
        elif option.lower() == 'carrera':
            # Verifica si el usuario es una instancia de la clase UserEstudiante
            if isinstance(user, UserEstudiante):
                # Pide al usuario que ingrese la nueva carrera
                new_major = input("Ingrese la nueva carrera: ")
                # Actualiza el atributo 'major' del usuario
                user.major = new_major
                # Muestra un mensaje de confirmación
                print("La carrera del usuario ha sido modificada exitosamente.")
            else:
                # Muestra un mensaje de error
                print("El usuario no es un estudiante, no puede modificar la carrera.")
        
        # Verifica si el usuario quiere modificar el departamento
        elif option.lower() == 'departamento':
            # Verifica si el usuario es una instancia de la clase UserTrabajador
            if isinstance(user, UserTrabajador):
                # Pide al usuario que ingrese el nuevo departamento
                new_department = input("Ingrese el nuevo departamento: ")
                # Actualiza el atributo 'department' del usuario
                user.department = new_department
                # Muestra un mensaje de confirmación
                print("El departamento del usuario ha sido modificado exitosamente.")
            else:
                # Muestra un mensaje de error
                print("El usuario no es un trabajador, no puede modificar el departamento.")
        
        # Si el usuario ingresa una opción inválida, muestra un mensaje de error
        else:
            print("Opción inválida, intente de nuevo.")
        
        # Abre el archivo de texto en modo escritura
        archivo = open("datos_usuarios.txt", "w")
        # Itera sobre la lista de usuarios registrados
        for user in self.usuarios_registrados:
            # Escribe los datos de cada usuario en el archivo, separados por "="
            archivo.write(user.firstName + "=" + user.lastName + "=" + user.email + "=" + user.username + "=")
            # Verifica si el usuario es estudiante o trabajador
            if isinstance(user, UserEstudiante):
                # Escribe la carrera del usuario
                archivo.write(user.major + "\n")
            else:
                # Escribe el departamento del usuario
                archivo.write(user.department + "\n")
        # Cierra el archivo
        archivo.close()
        
        # Termina la función
        return
    
    # Si no se encuentra al usuario, muestra un mensaje de error
       except StopIteration:
        print("No se encontró al usuario con ese nombre de usuario, intente de nuevo.")
        # Termina la función
        return

    
    def delete_user(self):
        # Pide al usuario que ingrese el nombre de usuario del usuario que quiere borrar
        username = input("Ingrese el nombre de usuario de su cuenta: ")
        # Intenta encontrar al usuario en la lista de usuarios registrados
        try:
            # Busca al usuario que tiene el nombre de usuario ingresado
            user = next(user for user in self.usuarios_registrados if user.username == username)
            # Muestra los datos de la cuenta a borrar
            print("Los datos de la cuenta a borrar son:")
            print(f"Nombre: {user.firstName}")
            print(f"Apellido: {user.lastName}")
            print(f"Correo: {user.email}")
            # Verifica si el usuario es estudiante o trabajador
            if isinstance(user, UserEstudiante):
             print(f"Carrera: {user.major}")
            else:
             print(f"Departamento: {user.department}")
             # Pregunta al usuario si está seguro de borrar su perfil
            opt = input("¿Está seguro que desea borrar todos los datos de su cuenta S/N?: ")
            # Si la opción es S, borra los datos de la lista de registrados
            if opt.upper() == "S":
              print(f"Se ha eliminado el perfil del usuario {user.username}")
              self.usuarios_registrados.remove(user)
              # Termina la función
              return
        # Si la opción es N, cancela la eliminación
            elif opt.upper() == "N":
             print("Se ha cancelado la eliminación del perfil")
            # Termina la función
             return
        # Si la opción es inválida, muestra un mensaje de error
            else:
             print("Opción inválida, intente de nuevo.")
            # Termina la función
            return
    # Si no se encuentra al usuario, muestra un mensaje de error
        except StopIteration:
         print("No se encontró al usuario con ese nombre de usuario, intente de nuevo.")
        # Termina la función
        return

    #GESTION DE MULTIMEDIA         
         
    def register_post(self):

        while True:
            # Pide el link de la foto o video a publicar
            multimedia=input("Ingrese el link de su publicacion:  ")
            # Valida que sea un link
            if multimedia.startswith("https://"):
                break

            else:
                print("Dato invalido, recuerde que debe ingresar un link")
        # Pide el username de la cuenta que realiza el post
        username=input("Ingrese su username para realizar esta publicacion:  ")
        #verifica que el username este en la lista de usuarios registrados
        try:
           user = next(user for user in self.usuarios_registrados if user.username == username)
           
           # Pide la descripcion que tendra el post
           caption=input("Ingrese la descripcion de su publicacion:  ")
           # Pide los hashtags que tendra el post
           hashtags=input("Ingrese los hashtags que quiera incluir en su publicacion:  ")
           #Pide la fecha que tendra el post
           date=input("Ingrese la fecha en la que realiza su publicación:  ")
           # Instancia la clase post usando los datos pedidos anteriormente
           publisher=user.id
           post=Post(username,multimedia,hashtags,caption,date,publisher)
           # Agrega el post a la lista de post_publicados
           self.post_publicados.append(post)
           
           # Imprime todos los datos con los que se registro el post 
           print(f"""Se ha realizado una publicación con los siguiente datos
              ------------------------------------------------------------
              Usuario:    {post.username}
              id:          {post.publisher}
              Multimedia: {post.multimedia}  
              tags:       {post.tags}
              caption:    {post.caption}
   fecha de publicacion:  {post.date}
                                       """)
        except StopIteration:
           print("No se ha encontrado el perfil con el nombre de usuario indicado")


         
        # Retorna el post creado
        return post
    
        
    

    # Modificar esta función para que reciba el nombre de usuario del usuario A
    def ver_post(self, username_a):
    # Buscar en la lista de usuarios registrados el objeto que corresponda al nombre de usuario del usuario A
     user_a = None
     for user in self.usuarios_registrados:
        if user.username == username_a:
            user_a = user
            break

    # Comprobar si se encontró el usuario A
     if user_a:
        # Pide al usuario que ingrese el nombre de usuario del usuario B
        usuario_b = input("Ingrese el nombre de usuario del usuario B: ")

        # Busca al usuario B en la lista de usuarios registrados en la aplicación
        try:
            # Busca al usuario que tiene el nombre de usuario ingresado
            user_b = next(user for user in self.usuarios_registrados if user.username == usuario_b)

            # Verifica si el usuario A sigue al usuario B o si es el mismo usuario
            if user_b.id == user_a.get_id() and user_a.is_following(user_b):
                # Itera sobre la lista de posts publicados por el usuario B
                for post in user_b.publications:
                    print("Username:", post.username)
                    print("Multimedia:", post.multimedia)
                    print("Hashtags:", post.tags)
                    print("Caption:", post.caption)
                    print("Date:", post.date)
                    print("Likes:", len(post.likes))
                    print("Comments:", len(post.comments))
                    opt=input("¿Quieres dar like a este post? S/N: ")
                    if opt.upper() == "S":
                        post.likes.append(user_a)
                        print("Has dado like a este post.")

            # Si el usuario A no sigue al usuario B, muestra un mensaje de error
            else:
                print("No puedes ver los posts de este usuario porque no lo sigues.")

        # Si no se encuentra al usuario B, muestra un mensaje de error
        except StopIteration:
            print("No se encontró al usuario con ese nombre de usuario, intente de nuevo.")



    def search_post(self):
     
     # Crea una lista vacía para almacenar los posts encontrados
     posts_encontrados = []
    
    # Pide al usuario que elija un filtro entre usuario o hashtag
     filtro = input("Ingrese el filtro que desea usar (usuario o hashtag): ")
    
    # Pide al usuario que ingrese el valor que desea buscar
     valor = input("Ingrese el valor que desea buscar: ")
    
    # Itera sobre la lista de posts obtenidos de la API
     for post in self.post_publicados:
        # Verifica si el filtro es 'usuario'
        if filtro.lower() == 'usuario':
            # Compara el valor del filtro con el atributo 'username' del post
            if valor.lower() == post.username.lower():
                # Agrega el post a la lista de posts encontrados
                posts_encontrados.append(post)
                print(f""" Post Encontrado
                      
                      Multimedia: {post.multimedia}
                      User que publica: {post.username}
                      Descripción:    {post.caption}
                      tags:        {post.tags}
                      Fecha de subida: {post.date}


                               """)
            else:
               print(f"El usuario {valor} no ha realizado ninguna publicacion")

        # Verifica si el filtro es 'hashtag'
        elif filtro.lower() == 'hashtag':
            # Verifica si el valor del filtro está en la lista de 'hashtags' del post
            if valor.lower() in post.tags:
                # Agrega el post a la lista de posts encontrados
                posts_encontrados.append(post)
                print(f""" Post Encontrado
                      
                      Multimedia: {post.multimedia}
                      User que publica: {post.username}
                      Descripción:    {post.caption}
                      tags:        {post.tags}
                      Fecha de subida: {post.date}


                               """)
            else:
               print(f"No hay posts con la/las etiqutas  {valor}")
    
    # Retorna la lista de posts encontrados
     return posts_encontrados         
        


    #GESTION DE INTERACCION

    def follow(self, username_a):
    # Buscar en la lista de usuarios registrados el objeto que corresponda al nombre de usuario del usuario A
     user_a = None
     for user in self.usuarios_registrados:
        if user.username == username_a:
            user_a = user
            break
    # Comprobar si se encontró el usuario A
     if user_a:
        # Solicitar el nombre de usuario del usuario B como input
        username_b = input(f"{user_a.username}, ingresa el nombre de usuario del usuario que quieres seguir: ")
        # Buscar en la lista de usuarios registrados el objeto que corresponda al nombre de usuario del usuario B
        user_b = None
        for user in self.usuarios_registrados:
            if user.username == username_b:
                user_b = user
                break
        # Comprobar si se encontró el usuario B
        if user_b:
            # Comprobar si los usuarios son del mismo tipo (estudiante o trabajador)
            if type(user_a) == type(user_b):
                # Comprobar si los usuarios son estudiantes y tienen la misma carrera
                if isinstance(user_a, UserEstudiante) and user_a.major == user_b.major:
                    # Seguir al usuario B automáticamente
                    user_a.followings.append(user_b.id)
                    print(f"{user_a.username} ha seguido a {user_b.username} porque estudian la misma carrera.")
                # Comprobar si los usuarios son trabajadores y tienen el mismo departamento
                elif isinstance(user_a, UserTrabajador) and user_a.department == user_b.department:
                    # Seguir al usuario B automáticamente
                    user_a.followings.append(user_b.id)
                    print(f"{user_a.username} ha seguido a {user_b.username} porque trabajan en el mismo departamento.")
                # Si no se cumple ninguna de las condiciones anteriores, pedir confirmación al usuario A
                else:
                    # Pedir al usuario A si quiere seguir al usuario B
                    respuesta = input(f"{user_a.username}, ¿quieres seguir a {user_b.username}? (S/N): ")
                    # Si la respuesta es afirmativa, seguir al usuario B
                    if respuesta.upper() == "S":
                        user_a.followings.append(user_b.id)
                        print(f"{user_a.username} ha seguido a {user_b.username}.")
                    # Si la respuesta es negativa, no hacer nada
                    elif respuesta.upper() == "N":
                        print(f"{user_a.username} no ha seguido a {user_b.username}.")
                    # Si la respuesta no es válida, mostrar un mensaje de error
                    else:
                        print("Respuesta no válida. Inténtalo de nuevo.")
            # Si los usuarios son de tipos diferentes, no permitir el seguimiento
            else:
                print(f"{user_a.username} no puede seguir a {user_b.username} porque son de tipos diferentes.")
        # Si no se encontró el usuario B, mostrar un mensaje de error
        else:
            print(f"No se encontró el usuario con el nombre de usuario {username_b}. Verifica que esté registrado en la aplicación.")
    # Si no se encontró el usuario A, mostrar un mensaje de error
     else:
        print(f"No se encontró el usuario con el nombre de usuario {username_a}. Verifica que esté registrado en la aplicación.")


    

    def unfollow(self, username_a):
    # Buscar en la lista de usuarios registrados el objeto que corresponda al nombre de usuario del usuario A
     user_a = None
     for user in self.usuarios_registrados:
        if user.username == username_a:
            user_a = user
            break
    # Comprobar si se encontró el usuario A
     if user_a:
        # Solicitar el nombre de usuario del usuario B como input
        username_b = input(f"{user_a.username}, ingresa el nombre de usuario del usuario que quieres dejar de seguir: ")
        # Buscar en la lista de usuarios registrados el objeto que corresponda al nombre de usuario del usuario B
        user_b = None
        for user in self.usuarios_registrados:
            if user.username == username_b:
                user_b = user
                break
        # Comprobar si se encontró el usuario B
        if user_b:
            # Comprobar si el usuario A sigue al usuario B
            if user_b.id in user_a.followings:
                # Dejar de seguir al usuario B
                user_a.followings.remove(user_b.id)
                print(f"{user_a.username} ha dejado de seguir a {user_b.username}.")
            # Si el usuario A no sigue al usuario B, mostrar un mensaje
            else:
                print(f"{user_a.username} no sigue a {user_b.username}. No puedes dejar de seguir a alguien que no sigues.")
        # Si no se encontró el usuario B, mostrar un mensaje de error
        else:
            print(f"No se encontró el usuario con el nombre de usuario {username_b}. Verifica que esté registrado en la aplicación.")
    # Si no se encontró el usuario A, mostrar un mensaje de error
     else:
        print(f"No se encontró el usuario con el nombre de usuario {username_a}. Verifica que esté registrado en la aplicación.")

        

    
    def main(self):
     
     self.get_user()
     self.get_post()
     
    # Imprime un mensaje de bienvenida
     print("Bienvenido a la aplicación de usuarios y publicaciones")
    # Crea un bucle para mostrar el menú de opciones
     while True:
        # Imprime el menú de opciones
        print("Seleccione una opción:")
        print("1. Registrar un usuario")
        print("2. Buscar un usuario")
        print("3. Modificar un usuario")
        print("4. Borrar un usuario")
        print("5. Registrar un post")
        print("6. Ver un post")
        print("7. Buscar un post")
        print("8. Seguir a un usuario")
        print("9. Dejar de seguir a un usuario")
        
        print("11. Salir")
        # Solicita al usuario que ingrese una opción
        option = input("Ingrese una opción: ")
        # Verifica si la opción es '1'
        if option == '1':
            # Llama a la función register_user de la instancia app
            self.register_user()
        # Verifica si la opción es '2'
        elif option == '2':
            self.search_user()
        # Verifica si la opción es '3'
        elif option == '3':
           self.modify_user()
        # Verifica si la opción es '4'
        elif option == '4':
           self.delete_user()
        # Verifica si la opción es '5'
        elif option == '5':
            self.register_post()
        elif option=="6":
           self.ver_post("cl10")
        elif option=="7":
           self.search_post()

        elif option=="8":
           self.follow("cl10")

        elif option=="9":
           self.unfollow("cl10")

        
            

        elif option=="11":
           print("Gracias por usar Metrogram, hasta luego.")
           break
            
        # Verifica si la opción es inválida
        else:
            # Imprime un mensaje de error
            print("Opción inválida. Por favor, ingrese una opción válida.")
        
     return

aplicacion=App()

aplicacion.main()
        






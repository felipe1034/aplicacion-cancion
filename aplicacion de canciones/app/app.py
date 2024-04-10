from flask import Flask, render_template, redirect, request, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'magaly2024'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agendaa2024"
)

cursor = db.cursor()  


def encripcontra(password):
    # Generar un hash de la contraseña
    encriptar = generate_password_hash(password)
    return encriptar

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        # Obtener las credenciales del formulario
        username = request.form.get('usuario')
        password = request.form.get('contrasena')

        # Consultar la base de datos para obtener el usuario
        cursor = db.cursor(dictionary=True)
        query = "SELECT usuarioper, contraper, rol FROM personas WHERE usuarioper = %s"
        cursor.execute(query, (username,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['contraper'], password):
            # Autenticación exitosa, establecer las variables de sesión
            session['usuario'] = usuario['usuarioper']
            session['rol'] = usuario['rol']

            # Redirigir según el rol del usuario
            if usuario['rol'] == 'Administrador':
                return redirect(url_for('lista'))
            else:
                return redirect(url_for('mostrar_canciones'))
        else:
            # Credenciales inválidas, mostrar mensaje de error
            print("Credenciales incorrectas. Por favor, intenta nuevamente.")
            return render_template('inicio.html')

    # Si la solicitud es GET, renderizar el formulario de inicio de sesión
    return render_template('inicio.html')

@app.route('/logout')
def logout():
    # Eliminar el usuario de la sesión
    session.pop('usuario', None)
    print("se cerro la sesion")
    return redirect(url_for('login'))

@app.route('/lista')
def lista():
    if 'usuario' in session:
        cursor.execute('SELECT * FROM personas')
        personas = cursor.fetchall()
        return render_template('index.html', personas=personas)
    else:
        return redirect(url_for('login'))

@app.route('/Registrar', methods=['GET', 'POST'])
def Registrar_usuario():
    if request.method == 'POST':
        Nombres = request.form.get('nombre')
        Apellidos = request.form.get('apellido')
        Email = request.form.get('email')
        Direccion = request.form.get('direccion')
        Telefono = request.form.get('telefono')
        Usuario = request.form.get('usuario')
        Contrasena = request.form.get('contrasena')
        Rol = request.form.get('txtrol')
        

        Contrasenaencriptada = generate_password_hash(Contrasena)

        cursor.execute("SELECT * FROM personas WHERE usuarioper = %s", (Usuario,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('el usuario ya existe')
            return redirect(url_for('Registrar_usuario'))

        cursor.execute("INSERT INTO personas(nombreper, apellidoper, emailper, direccionper, telefonoper, usuarioper, contraper,rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Contrasenaencriptada, Rol))
        db.commit()
        print('Usuario creado satisfactoriamente')

        return redirect(url_for('lista'))
    return render_template('Registrar.html')



@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombper = request.form.get('nombre_usuario')
        apellidoper = request.form.get('apellido_usuario')
        emailper = request.form.get('email_usuario')
        dirper = request.form.get('direccion_usuario')
        telper = request.form.get('telefono_usuario')
        usuarioper = request.form.get('usuario_usuario')
        passper = request.form.get('contrasena_usuario')
        rol = request.form.get('txtrol')
        Contrasena = generate_password_hash(passper)

        sql = "UPDATE personas SET nombreper=%s, apellidoper=%s, emailper=%s, direccionper=%s, telefonoper=%s, usuarioper=%s, contraper=%s,rol=%s WHERE polper=%s"
        cursor.execute(sql, (nombper, apellidoper, emailper, dirper,telper, usuarioper,Contrasena,rol, id))
        
        db.commit()
        print('Usuario actualizado correctamente')
        return redirect(url_for('lista'))
    else:
        cursor = db.cursor()   
        cursor.execute("SELECT * FROM personas WHERE polper = %s", (id,))
        data = cursor.fetchall()
        cursor.close()
        return render_template('edit.html', personas=data[0])

@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
        cursor.execute('DELETE FROM personas WHERE polper = %s', (id,))
        db.commit()
        print('Usuario eliminado correctamente') 
        return redirect(url_for('lista'))
    

  

    
@app.route('/Registro', methods=['GET', 'POST'])
def registro_cancion():
    if request.method == 'POST':
       Titulo = request.form.get('titulo')
       Artista = request.form.get('artista')
       Genero = request.form.get('genero')
       Precio = request.form.get('precio')
       Duracion = request.form.get('duracion')
       Lanzamiento = request.form.get('lanzamiento')

       cursor = db.cursor()
       cursor.execute(
           "SELECT * FROM canciones WHERE titulo = %s or artista = %s", (Titulo, Artista))
       existing_song = cursor.fetchone()
       if existing_song:
           flash('Canción ya existe')
           return redirect(url_for('cancion.html'))

       cursor.execute("INSERT INTO canciones(titulo, artista, genero, precio, duracion, lanzamiento) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                      (Titulo, Artista, Genero, Precio, Duracion, Lanzamiento))
       db.commit()

       flash('Canción registrada correctamente', 'success')
       return redirect(url_for('lista'))  # Redirigir a la página principal
    return render_template("index.html")

#enlazar actualizar
@app.route('/actualizar/<int:id>',methods=['GET', 'POST'])
def editar_cancion(id):
    cursor = db.cursor()
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        artista = request.form.get('artista')
        genero = request.form.get('genero')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')
        lanzamiento = request.form.get('lanzamiento')

        sql = "UPDATE canciones set titulo=%s,artista=%s,genero=%s,precio=%s,duracion=%s,lanzamiento=%s, where id_can=%s"
        cursor.execute(sql,(titulo,artista,genero,precio,duracion,lanzamiento,id)) 
        db.commit()
        
        return redirect(url_for('listar'))
    
    else: 
        cursor = db.cursor()
        cursor.execute('SELECT * FROM canciones WHERE id_canciones=%s' ,(id,))
        data = cursor.fetchall()

        return render_template('index.html', canciones=data[0])

@app.route("/eliminarc/<int:id>", methods=['GET'])
def eliminar_cancion(id):

    cursor = db.cursor()
    cursor.execute('DELETE FROM canciones WHERE id_cancion = %s', (id,))
    db.commit()
    return redirect(url_for('listar'))


if __name__ == '__main__':
    app.add_url_rule('/', view_func=lista)
    app.run(debug=True, port=5005)
   

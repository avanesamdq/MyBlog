from flask import render_template, Blueprint, flash, g, redirect, request,url_for
# werkzeug.exceptions para manejar errores
from werkzeug.exceptions import abort 
from myblog.models.post import Post
from myblog.models.user import User
from myblog.views.auth import login_required
from myblog import db
from datetime import datetime
from myblog import app
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'myblog\\static\\arch'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# registrar en blueprint

blog = Blueprint('blog', __name__)

# crear funcion para obtener un ususario mediante el id
# OBTENER UN USUARIO
def get_user(id):
    user= User.query.get_or_404(id)
    return user

# LISTAR TODOS LOS POST 
@blog.route('/') 
def index():
    posts = Post.query.all()  
    posts = list(reversed(posts))
    db.session.commit()
    return render_template('blog/index.html', posts = posts, get_user = get_user)
    

# REGISTRAR O CREAR UNA PUBLICACION 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blog.route('/blog/create', methods = ('GET','POST'))
@login_required # si no esta logueado esta funcion queda deshabilitada
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        im = request.files.get('file')

         #comprobar si la solicitud de publicación tiene la parte del archivo
        if 'file' not in request.files:
            flash('Sin parte de archivo')
            return redirect(request.url)
        file = request.files['file']
         #Si el usuario no selecciona un archivo, el navegador envía un
         #archivo vacío sin nombre de archivo.
        if file.filename == '':
            flash('Archivo No Seleccionado')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        post = Post(g.user.id, title, body, im.filename)
        error = None
        if not title:
            error = 'Se requiere un titulo.'
        if error is not None:
            flash(error)
        else: 
            db.session.add(post)
            db.session.commit() 
            return redirect(url_for('blog.index', name=filename))
        flash(error)
        flash('Publicación enviada correctamente.')
    return render_template('blog/create.html')

def get_post(id, check_author = True):
    post = Post.query.get(id)
    if post is None:
        abort(404, f'Id {id} de la publicacion no existe')
    if check_author and post.author != g.user.id:
        abort(404)
    return post 


# UPDATE POST
# para actualizar necesito obtener el id, indicar int para recibir ese valor q voy
# a recibir mediante url a entero. xq todo lo que recibimos mediante url va a ser de
# tipo string. con esto indicamos que va a ser tipo int
@blog.route('/blog/update/<int:id>', methods = ('GET','POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        post.created = datetime.now()

        error = None
        if not post.title:
            error = 'Se requiere un titulo'
        if error is not None:
            flash(error)
        else:
            db.session.add(post)  
            db.session.commit()
            return redirect(url_for('blog.index'))
        flash(error)
    return render_template('blog/update.html', post = post)

# ELIMINAR UN POST 
@blog.route('/blog/delete/<int:id>')
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
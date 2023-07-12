import functools
from flask import render_template, Blueprint, flash, g, redirect, request, session,url_for
from myblog.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from myblog import db 


auth = Blueprint('auth', __name__, url_prefix= '/auth')

# REGISTRAR UN USUARIO 
@auth.route('/register', methods = ('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username, generate_password_hash(password))

        error = None
        if not username:
            error = 'Se requiere nombre de Usuario.'
        elif not password:
            error = 'Se requiere una Contrasena.'

        # query para consultar a la db 
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'el usuario {username} ya esta registrado'
        flash(error)
    return render_template('auth/register.html')


# INICIAR SESION 
@auth.route('/login', methods = ('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None

        user = User.query.filter_by(username = username).first()

        if user == None:
            error = 'Nombre de usuario no existe.'
        elif not check_password_hash(user.password, password):
            error = 'Contrasena Incorrecta.'

        if error is None:
            session.clear()
            session ['user_id'] = user.id
            return redirect(url_for('blog.index'))
        flash(error)
    return render_template('auth/login.html')


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


# CERRAR SESION 
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

'''la funcion (login_required) va a recibir como argumento una vista
porque aqui voy a decorar a esas vistas que necesitan loguearse, aqui voy a recibir una 
funcion que va hacer practicamente la vista que requieren loguearse..
luego utilizo un decorador, este decorador va a decorar otra funcion
el cual va a verificar si esta logueado o no y luego de eso va a retornarlo a la parte de 
login si es q no esta logueado '''

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login')) # a esta vista tiene q redireccionar
        return view(**kwargs)# y si esta logueado simplemente va a retornar la vista
    return wrapped_view # por ultimo va a retornar la funcion que va hacer decorada o la funcion q va a decorar  

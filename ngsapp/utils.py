import os
import secrets
from functools import wraps

from PIL import Image
from flask import current_app, url_for, flash, abort
from flask_jwt_extended import current_user, verify_jwt_in_request, jwt_required
from werkzeug.utils import secure_filename, redirect


def img_upload(file_storage, resize=(450, 450), base_dir='protected', allowed=None):
    if allowed is None:
        allowed = ['png', 'jpg', 'jpeg', 'gif']
    filename = secure_filename(file_storage.filename)
    ext = filename.split('.')[-1]
    if not (ext in allowed):
        return {'message': dict(error='file extension not allowed', other='allowed extensions are', extensions=allowed)}
    cur_file_name = f'{secrets.token_hex(20)}.{ext}'
    path = os.path.join(current_app.root_path, 'static', f'{base_dir}/{cur_file_name}')
    ret = {'filename': cur_file_name, 'upload': file_storage, 'full_path': path}
    image = Image.open(file_storage)
    image.thumbnail(resize)
    ret['upload'] = image
    return ret


def delete_file(filename, base_dir='protected'):
    path = os.path.join(current_app.root_path, 'static', f'{base_dir}/{filename}')
    if not os.path.isfile(path):
        return {'message': dict(error='File Not Found')}
    os.remove(path)
    return {'message': dict(success='File removed')}


def file_upload(file_storage, base_dir='protected', allowed=None):
    if allowed is None:
        allowed = ['pdf', 'docx', 'doc', 'zip', 'png', 'jpg', 'jpeg', 'gif']
    filename = secure_filename(file_storage.filename)
    ext = filename.split('.')
    if not (ext[-1] in allowed):
        return {'error': 'file extension not allowed', 'other': 'allowed extensions are',
                'extensions': allowed}
    cur_file_name = f'{"".join(ext[:-1])}_{secrets.token_hex(20)}.{ext[-1]}'
    path = os.path.join(current_app.root_path, 'static', f'{base_dir}/{cur_file_name}')
    ret = {'filename': cur_file_name, 'upload': file_storage, 'full_path': path}
    return ret


def roles_required(roles):
    def wrapper(func):
        @wraps(func)
        def decorate(*args, **kwargs):
            if not (current_user.role in roles):
                return {"message": "Unauthorized"}, 401
            return func(*args, **kwargs)

        return decorate

    return wrapper


def app_roles_required(roles):
    def wrapper(func):
        @wraps(func)
        def decorate(*args, **kwargs):
            if not (current_user.role in roles):
                return abort(403)
            return func(*args, **kwargs)
        return decorate
    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            flash('Please login to access this page', 'info')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return wrapper

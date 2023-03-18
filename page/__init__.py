import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('user_html', __name__, url_prefix='/user')


@bp.route("/create_user", methods=['GET'])
def createUserHtml():
    return '''
        <form method="post" action="/user">
            <p>Name <input type=text name=name>
            <p>Login <input type=text name=login>
            <p>Pass <input type=text name=pass>
            <p><input type=submit value=Create>
        </form>
    '''


@bp.route("/put_user", methods=['GET'])
def putUserHtml():
    return '''
        <form method="PUT" action="/user/1">
            <p>id <input type=text name=id>
            <p>Name <input type=text name=name>
            <p><input type=submit value=Update>
        </form>
    '''

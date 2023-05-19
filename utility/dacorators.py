import functools

from flask import redirect, url_for, session

from auth.models import User


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(ctx, **kwargs):
        user=User.query.filter(User.id==session.get('uid')).first()
        if user is None:
            return redirect(url_for('login'))

        return view(ctx, **kwargs)

    return wrapped_view
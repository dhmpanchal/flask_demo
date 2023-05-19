import json
import re
from flask.views import View
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import generate_password_hash, check_password_hash

from post.models import Posts
from .models import User
from database import db_session
from utility.dacorators import login_required

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

class IndexView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        current_user=User.query.filter(User.id==session.get('uid')).first()
        return render_template("index.html", params=params, current_user=current_user)

class AboutView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        current_user=User.query.filter(User.id==session.get('uid')).first()
        return render_template("about.html", params=params, current_user=current_user)

class ContactView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        current_user=User.query.filter(User.id==session.get('uid')).first()
        return render_template("contact.html", params=params, current_user=current_user)

class DashboardView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        current_user=User.query.filter(User.id==session.get('uid')).first()
        posts = Posts.query.filter(Posts.user_id==current_user.id)
        return render_template("dashboard.html", params=params, current_user=current_user, posts=posts)

class SignUpView(View):
    methods = ['GET', 'POST']

    def validate_password(self, password):
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$'
        return bool(re.match(regex, password))
    
    def dispatch_request(self):
        values = {}
        if request.method == 'POST':
            fullname = request.form.get('fullname')
            phone = request.form.get('phone')
            email = request.form.get('email')
            password = request.form.get('password')

            user=User.query.filter(User.email==email).first()

            if user is None:
                hashed_pwd = generate_password_hash(password, 10)
                the_new_user = User(fullname=fullname, email=email, phone=phone, password=hashed_pwd)
                db_session.add(the_new_user)
                db_session.commit()

                flash('User created successfully!', 'success')
                return redirect('/register')
            else:
                values = {
                    'fullname': fullname,
                    'phone': phone,
                    'email': email,
                }
                flash('User is already exist with given email!', 'danger')
                return render_template("signup.html", params=params, values=values)

        return render_template("signup.html", params=params, values=values)

class LoginView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user=User.query.filter(User.email==email).first()
            if user is not None:
                if check_password_hash(user.password, password):
                    session.clear()
                    session['uid'] = user.id
                    return redirect('/')
                else:
                    flash('Incorrect Password!', 'danger')
                    return render_template("login.html", params=params)
            else:
                flash('User is not found!', 'danger')
                return render_template("login.html", params=params)
        return render_template("login.html", params=params)

class LogoutView(View):
    def dispatch_request(self):
        session.clear()
        return redirect('/login')
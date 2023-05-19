import json
import datetime
import os
from flask.views import MethodView
from flask import render_template, redirect, request, session, flash, url_for
from auth.models import User
from utility.dacorators import login_required
from .models import Posts
from database import db_session

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

class AddPostView(MethodView):
    @login_required
    def get(self):
        current_user=User.query.filter(User.id==session.get('uid')).first()
        return render_template("add_post.html", params=params, current_user=current_user)
    
    def post(self):
        title=request.form.get('title')
        slug=request.form.get('slug')
        content=request.form.get('content')
        tagline=request.form.get('tagline')
        img_file= request.files['img_file']
        
        current_user=User.query.filter(User.id==session.get('uid')).first()
        
        #upload the image
        dir = os.getcwd()
        path = f'{dir}/static/img'
        url=os.path.join(path, img_file.filename)
        img_file_path=os.path.join('/static/img', img_file.filename)
        img_file.save(url)

        the_new_post = Posts(title=title, slug=slug, content=content, tagline=tagline, date=datetime.datetime.now().strftime('%Y-%m-%d'), img_file=img_file_path, user_id=current_user.id)
        db_session.add(the_new_post)
        db_session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('add-post'))

class EditPostView(MethodView):
    @login_required
    def get(self, slug):
        current_user=User.query.filter(User.id==session.get('uid')).first()
        post=Posts.query.filter(Posts.slug==slug).first()
        return render_template("edit_post.html", params=params, current_user=current_user, post=post)
    
    def post(self, slug):
        title=request.form.get('title')
        slug=request.form.get('slug')
        content=request.form.get('content')
        tagline=request.form.get('tagline')
        img_file= request.files['img_file']
        img_file_path = ''
        
        post=Posts.query.filter(Posts.slug==slug).first()
        if post:
            #upload the image
            if img_file:
                dir = os.getcwd()
                path = f'{dir}/static/img'
                url=os.path.join(path, img_file.filename)
                img_file_path=os.path.join('/static/img', img_file.filename)
                img_file.save(url)

            post.title = title
            post.slug = slug
            post.content = content
            post.tagline = tagline
            post.img_file = img_file_path if img_file else post.img_file
            db_session.commit()

            flash('Post updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Post not found!', 'danger')
            return redirect(f'/post/edit/{slug}')
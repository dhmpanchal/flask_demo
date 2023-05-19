from flask import Flask
from auth.views import AboutView, ContactView, DashboardView, IndexView, LoginView, LogoutView, SignUpView
from post.views import AddPostView, EditPostView

app = Flask(__name__)

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/about', view_func=AboutView.as_view('about'))
app.add_url_rule('/contact', view_func=ContactView.as_view('contact'))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))

#post routes
app.add_url_rule('/post/add', view_func=AddPostView.as_view('add-post'))
app.add_url_rule('/post/edit/<slug>', view_func=EditPostView.as_view('edit-post'))

# Authentication routes
app.add_url_rule('/register', view_func=SignUpView.as_view('register'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
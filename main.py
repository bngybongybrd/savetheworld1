from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, PostForm
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user, login_required
import sqlite_code
import sqlite3
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b50ac89557ebfa192ed90596cbaa2dfd'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

class User(UserMixin):
    def __init__(self, rowid, username, email, password):
      self.rowid = rowid
      self.username = username
      self.email = email
      self.password = password
      self.authenticated = False
    def is_active(self):
      return True
    def is_anonymous(self):
      return False
    def is_authenticated(self):
      return self.is_active
    def get_id(self):
      return self.rowid


@login_manager.user_loader
def load_user(row_id):
  conn = sqlite3.connect('user_database.db')
  curs = conn.cursor()
  curs.execute("SELECT rowid, * from user_database where rowid = (?)", [row_id])
  lu = curs.fetchone()
  if lu is None:
    return None
  else:
    return User(int(lu[0]), lu[1], lu[2], lu[3])


'''posts = [{
  'user': 'John',
  'title': 'Post 1',
  'content': 'Help',
  'date': 'March 3, 2023'
}, {
  'user': 'Tim',
  'title': 'Post 2',
  'content': 'Help',
  'date': 'March 4, 2023'
}]'''

@app.route("/")
@app.route("/home")
def home():
  #p = current_user.username
  posts = sqlite_code.show_all_posts()
  items = sqlite_code.show_all_users()
  return render_template('home.html', posts=posts, items=items)


@app.route("/about")
def about():
  return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    sqlite_code.add_user(form.username.data, form.email.data, form.password.data)
    flash(f'Account created for {form.username.data}! You can now log in', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    if sqlite_code.email_lookup(form.email.data) and sqlite_code.pw_check(form.password.data ,form.email.data):
      user = sqlite_code.get_user_with_email(form.email.data)
      Us = load_user(user[0])
      login_user(Us, remember=form.remember.data)
      next_page = request.args.get('next')
      flash("Logged in successfully", "success")
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash("Logged in unsuccessful. Please check your input", "danger")
  return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
  return render_template('account.html', title='Account')

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    user = sqlite_code.get_user_with_rowid(current_user.get_id())
    sqlite_code.add_post(user[1], form.title.data, form.content.data, str(datetime.date.today()))
    flash('Your post has been created!', 'success')
    return redirect(url_for('home'))
  return render_template('create_post.html', title='New Post', form=form)

  
app.run(host='0.0.0.0', port=81)

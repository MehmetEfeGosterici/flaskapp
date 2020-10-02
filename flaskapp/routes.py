from flask import render_template, request, redirect, url_for, flash
from flaskapp.forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm
from flaskapp.models import User, Post
from flaskapp import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
def home():
    return render_template("base.html")

@app.route("/posts")
def posts():
    all_posts = Post.query.all()
    return render_template("index.html", posts=all_posts, title="posts")

@app.route("/posts/new_post"  ,methods=["POST","GET"])
def newpost():
    form = PostForm()
    if request.method == "POST":
        post_title = form.title.data
        post_content = form.content.data
        new_task = Post( title=post_title, content=post_content, author=current_user)
        db.session.add(new_task)
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("add.html", title="add post", form=form)

@app.route("/posts/edit/<int:id>"  ,methods=["POST","GET"])
@login_required
def edit(id):
    form = PostForm()
    post = Post.query.get_or_404(id)
    if request.method == "POST":
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for("posts"))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("add.html", form=form, post=post)

@app.route("/posts/delete/<int:id>", methods=["POST","GET"])
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts"))


@app.route("/register", methods=["POST","GET"])
def register():
    
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(Username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'account created for {form.username.data}!','success')
        return redirect(url_for('posts'))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page)if next_page else redirect(url_for('posts'))
        else:
            flash(f'Login failed please check your info', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.Username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated","success")
        return redirect(url_for("account"))
    image_file = url_for('static', filename= current_user.user_image)
    return render_template("account.html", title="account", image_file=image_file, form=form)


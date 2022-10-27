from flask_app import app, render_template, request, redirect, bcrypt, session, flash
from flask_app.models.user import User


# ! CREATE

@app.route("/")
def index():
    # call the get all classmethod to get all friends
    print(dir(bcrypt))
    return render_template("index.html")


@app.route('/register/user', methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    user_id = User.save(user_data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']

    return redirect('/recipes')


@app.route("/login", methods=['POST'])
def login():
    # check the db for the email entered
    print(request.form)
    user = User.get_by_email(request.form)
    if not user:
        flash("invalid credentials")
        return redirect('/')
    password_valid = bcrypt.check_password_hash(user.password, request.form['password'])
    if not password_valid:
        flash("invalid credentials")
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/recipes')


@app.route('/show/user')
def show_user():
    data = {'id': session['user_id']}
    return render_template('show_user.html', user=User.get_one_with_recipes(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
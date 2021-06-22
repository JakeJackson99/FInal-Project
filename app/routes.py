"""The logic for the various routes of the program.

When the user enters a specific URL, such as '/about', the corresponding route function
is performed such as to render the about page's HTML. There are various routes,
from returning the index page to querying the database for the dashboard page.
"""

from flask import render_template, url_for, redirect, flash, request, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.sql import func
import time

from app import app, db, feed_content, SEND, MAX, HEADING, CONTENT
from app.forms import LoginForm, DataForm
from app.models import User, UserBehaviours


# Pages: index, dashboard, experiment, admin_login, experiment_form

@app.route('/')
def index():
    """The index page.

    Returns:
        The index page.
    """
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """The dashboard page for the admin user - login required.

    Returns:
        The dashboard page if the user is logged in.
    """

    return render_template('dashboard.html')


@app.route('/experiment')
def experiment():
    """The experiment page.

    Returns:
        The experiment page.
    """
    return render_template('experiment.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """The admin login page.

    Returns:
        The admin login page if the user is not logged in. Otherwise, it
        redirects them to dashboard().
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin_login'))

        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('dashboard'))

    return render_template('admin_login.html', form=form)


@app.route('/experiment_form', methods=['GET', 'POST'])
def experiment_form():
    """The data form for the user to add additional information.

    If the user does not want to add any additional information they can still
    take part in the experiment; including information just allows for more
    in-depth analytics via the dashboard.

    Returns:
        The form page if the user has submitted nothing or the submission is
        not valid. Otherwise, it redirects them to the experiment().
    """
    form = DataForm()
    genders = ['Male', 'Female', 'Other']

    if form.validate_on_submit():
        if form.age.data >= 13 and form.age.data < 100 and \
            form.gender.data in ['Male', 'Female', 'Other']:
            session['age'] = form.age.data
            session['gender'] = form.gender.data
        else:
            flash('Invalid input')
            return redirect(url_for('experiment_form'))

        return redirect(url_for('experiment'))

    return render_template('experiment_form.html', form=form, 
                            ages=[x for x in range(13, 100)], 
                            genders=genders)


# Functional routes: load, experiment/submit, daashboard/chart_data, logout

@app.route('/load')
def load():
    """Loads x amount of data for the frontend.
    
    If type "endless" (1) is passed as an argument in the URL, then and endless
    stream of data is sent. Otherwise, a feed of data up until "c" is sent.

    Returns:
        A JSON-formatted object storing the data for the feed.
    """

    time.sleep(0.5)

    if request.args:
        c = int(request.args.get('c'))
        type = int(request.args.get('page_type'))

    if type == 1:
        print(f'ENDLESS loading; page type: {type}')
        print(f'Returning posts {c} to {c + SEND}')

        feed_content2 = list()
        for x in range(SEND):
            feed_content2.append([HEADING, CONTENT])

        response = jsonify(feed_content2[0:SEND])

    elif type == 2:
        print(f'DISCRETE loading; page type: {type}')

        if c == MAX:
            print('No more posts')
            response = jsonify({})
        else:
            print(f'Returning posts {c} to {c + SEND}')
            response = jsonify(feed_content[c:c+SEND])

    return response


@app.route('/experiment/submit', methods=['POST'])
def submit_data():
    """Handles the submitted data storing the user's behaviours and stores
    them in the database.

    Returns:
        A message for the frontend. Not necassary, but a return value is
        required.
    """

    req = request.get_json()

    endless = req["page_type"] == 1
    time_seconds = req["time"]
    age = session.get("age")
    gender = session.get("gender")

    print(
        f'Data received | time: {time_seconds}, page type: {endless}, age: {age}, gender: {gender}')

    entry = UserBehaviours(
        endless=endless, time_seconds=time_seconds, age=age, gender=gender)
    db.session.add(entry)
    db.session.commit()

    return "Message received"


@app.route('/dashboard/chart_data', methods=['POST', 'GET'])
@login_required
def chart_data():
    """Sends the data responsible for populating the charts on the dashboard.

    Returns:
        A JSON-formatted object storing all the data for the charts.
    """
    discrete_time = \
        db.session.query(func.avg(UserBehaviours.time_seconds)).filter(
            UserBehaviours.endless.is_(False)).scalar()

    endless_time = \
        db.session.query(func.avg(UserBehaviours.time_seconds)).filter(
            UserBehaviours.endless.is_(True)).scalar()

    male_time = db.session.query(func.avg(UserBehaviours.time_seconds)).filter(
        UserBehaviours.gender.is_("Male")).scalar()

    female_time = db.session.query(func.avg(UserBehaviours.time_seconds)).filter(
        UserBehaviours.gender.is_("Female")).scalar()

    response = {
        "endless_time": round(endless_time, 1),
        "discrete_time": round(discrete_time, 1),
        "male_time": round(male_time, 1),
        "female_time": round(female_time, 1)
    }

    return jsonify(response)


@ app.route('/logout')
def logout():
    """Logs the user out (Flask-Login).

    Returns:
        The index page.
    """

    logout_user()
    return redirect(url_for('index'))

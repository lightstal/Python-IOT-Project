from flask import render_template, url_for, flash, redirect, request, Blueprint
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import matplotlib.pyplot as plt
import os

import requests
import json
import re

abs_path = os.path.dirname(os.path.abspath(__file__))

def formatDateTime(dateTime):
    a = re.sub(r'[A-Z]', ' ', dateTime).rstrip().split()
    b = a[0].split('-')
    b[0], b[1] = b[2], b[1]
    b = '-'.join(b[:2])
    return f"{b} {a[1]}"


def get_data(url):
    temp = []
    humidity = []
    timings = []
    raw_data = [[], [], []]
    try:
        response = requests.get(url)
        data = json.loads(response.content)
        print(data)
        for i in data['feeds']:
            formattedtime = formatDateTime(i['created_at'])

            temp.append(convertToInt(i['field1']))
            raw_data[0].append(convertToInt(i['field1']))
            humidity.append(convertToInt(i['field2']))
            raw_data[1].append(convertToInt(i['field2']))

            timings.append(formattedtime)
            raw_data[2].append(formattedtime)
        print(humidity)
        return temp, humidity, timings, raw_data
    except:
        print("Error retrieving data")


def convertToInt(data):
    if not data:
        return data
    try:
        f = float(data)
        i = int(f)
        return i if f == i else f
    except ValueError:
        return data


posts = [
    {
        'author': 'Bryan Kor',
        'title': 'Blog Post 1',
        'content': 'This safe really has exceeded my expectations for a safe. I am so happy I found it. Comes with not just web monitoring but also social media!',
        'date_posted': '7th December, 2021'
    },
    {
        'author': 'Goh Xu Hao',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': '7th December, 2021'
    }
]


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html', var=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can log in now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/account')
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/graph')
def graph():
    plotting()
    return render_template('graph.html', title='Graph', url='static/images/graph.png')

def plotting():
    temp_list, humidity_list, timings_list, raw_data_list = get_data(
        "https://api.thingspeak.com/channels/1585193/feeds.json?results=2000000")
    fig, ax1 = plt.subplots()
    plt.ioff()
    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature', color=color)
    # int_temp = [int(item) for item in temp_list]
    ax1.plot(timings_list, temp_list, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Humidity', color=color)  # we already handled the x-label with ax1
    ax2.plot(timings_list, humidity_list, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.autofmt_xdate(rotation=90, ha="right")
    fig.subplots_adjust(hspace=0.5, bottom=0.3)
    fig.suptitle('Temperature and Humidity')
    plt.show()
    fig.savefig(abs_path + '\\static\\images\\graph.png')
    plt.show()



@app.route('/data')
def data():
    temp_list, humidity_list, timings_list, raw_data_list = get_data(
        "https://api.thingspeak.com/channels/1585193/feeds.json?results=2000000")
    return render_template('data.html', temp_list=temp_list, humidity_list=humidity_list, timings_list=timings_list,
                           raw_data_list=raw_data_list)

# @app.route('/data')
# def data():


# def main():
#     plotting()

from . import database
from werkzeug.security import check_password_hash, generate_password_hash   #never store a password as the password itself
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .sql_struct import User

authentication = Blueprint('authentication', __name__) #defines the blueprint

@authentication.route('/sign-up', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        email_address = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirm')
        account = User.query.filter_by(email=email_address).first()
        if account:
            flash('This Email Already Exists In Our System. Please Try Another One.', category='error')
        elif email_address == "":
            flash("Please enter your email.", category='error')
        elif first_name == "":
            flash("Please enter your first name.", category='error')
        elif last_name == "":
            flash("Please enter your last name.", category='error')
        elif password == None or password == "":
            flash("Please enter a password.", category='error')
        elif password_confirmation == None or password_confirmation == "":
            flash("Please confirm your password.", category='error')
        elif len(first_name) < 2:
            flash('Your First Name Should Be Longer Than 1 Character', category='error')
        elif len(last_name) < 2:
            flash('Your Last Name Should Be Longer Than 1 Character', category='error')
        elif(password != password_confirmation):
            flash('The Passwords Entered Don\'t Match. Please Try Again.', category='error')
        elif len(password) < 8:
            flash('Your Password Should Be Longer Than 7 Characters. Please Try Again.', category='error')
        elif len(email_address) < 5:
            flash('Your Email Should Be Longer Than 4 Characters. Please Try Again.', category='error')
        #add checks for symbols and @ in email
        else: #add user to the database
            save_new_password = generate_password_hash(password, method='sha256')
            generate_user = User(email=email_address, first_name=first_name, last_name=last_name, password=save_new_password)
            database.session.add(generate_user) #adds user to the database
            database.session.commit()
            login_user(generate_user, remember=True)
            flash('User Account Has Been Created Successfully. Welcome ' + first_name + " " + last_name, category='success')
            return redirect(url_for('notelist.start'))


    return render_template("new_user.html", user=current_user)


@authentication.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email_address = request.form.get('email')
        password = request.form.get('password')
        account = User.query.filter_by(email=email_address).first() #filter database by given email
        if not account:
            flash('The Email Entered is Not In Our System. Please Try Again.', category='error')
        else:
            if not check_password_hash(account.password, password):
                flash('The Password Entered is Incorrect. Please Try Again.', category='error')
            else:
                flash('You Have Logged In Successfully! Welcome ' + account.first_name + " " + account.last_name, category='success')
                login_user(account, remember=True)
                return redirect(url_for('notelist.start'))
            
    return render_template("existing_user.html", user=current_user)

@authentication.route('/logout')
@login_required
def user_logout():
    logout_user()
    flash("You Have Been Logged Out Successfully. Have A Nice Day.")
    return redirect(url_for('authentication.user_login'))

from flask import render_template, url_for, flash, redirect, request, Blueprint, make_response
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        # Ищем пользователя по username
        user = User.query.filter_by(username=form.username.data).first()

        # Проверяем пароль
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.account'))
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    response = make_response(redirect(url_for('main.home')))
    response.delete_cookie('remembered_email')
    return response

@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@main.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('main.account'))
        else:
            flash('Old password is incorrect.', 'danger')
    return render_template('change_password.html', title='Change Password', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            # Проверяем, существует ли пользователь с таким email
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Этот email уже зарегистрирован. Пожалуйста, используйте другой email.', 'danger')
                return render_template('register.html', form=form)

            # Проверяем, существует ли пользователь с таким именем
            existing_username = User.query.filter_by(username=form.username.data).first()
            if existing_username:
                flash('Это имя пользователя уже занято. Пожалуйста, выберите другое.', 'danger')
                return render_template('register.html', form=form)

            # Если все проверки пройдены, создаем пользователя
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password
            )

            db.session.add(user)
            db.session.commit()

            flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
            return redirect(url_for('main.login'))

        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.', 'danger')

    return render_template('register.html', title='Регистрация', form=form)
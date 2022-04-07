from flask import Flask, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash

from data.users import User
from forms.form import RegisterForm
from data.db_session import global_init, create_session

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
global_init("db/db.db")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template("register.html", form=form, message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(form.login_or_email.data == User.email).first():
            return render_template("register.html", form=form, message="Такой пользователь уже есть")
        user = User(
            email=form.login_or_email.data,
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/success")

    return render_template("register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)

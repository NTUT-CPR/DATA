from flask import redirect, url_for, render_template, session, flash
from flask.ext.login import current_user, login_required, logout_user, login_user

from FlaskMVC.service import get_blueprint
from FlaskMVC.models.db.User import User, AccessLevel
from FlaskMVC.models.form.LoginForm import LoginForm
from FlaskMVC.models.units.tools import password_encryption, required_to_flash
from FlaskMVC.models.units.login import backstage_required

admin = get_blueprint('admin')


@admin.route('/', methods=['GET', 'POST'])
def index():
    """
    登入後台
    :return: 登入後臺頁面
    """
    def login_redirect():
        return redirect(url_for('admin.page'))

    if current_user.is_anonymous is not True:
        return login_redirect()

    form = LoginForm()
    if form.validate_on_submit():
        admin_user = User.query.filter_by(account=form.name.data, password=password_encryption(form.password.data)).first()
        if admin_user is not None:
            session['level'] = admin_user.level
            login_user(admin_user)
            return login_redirect()
        else:
            flash('帳號或密碼錯誤')
    required_to_flash(form)
    return render_template('admin/index.html', form=form)


@admin.route('/logout')
@login_required
@backstage_required
def logout():
    """
    登出後台
    :return: 轉址到登入後台
    """
    logout_user()
    return redirect(url_for('admin.index'))


@admin.route('/page')
@login_required
@backstage_required
def page():
    return render_template('admin/page.html', name=current_user.name)
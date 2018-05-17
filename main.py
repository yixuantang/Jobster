from __future__ import print_function
from flask import Flask
from flask import request, render_template, jsonify, make_response, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from forms import *
from auth import User
from functions import *



'''

TODO:
- Add some dummy content on the home page
- Add search sql query
- Add "mark as read" query
- Apply/post job queries
- Error in registration: IntegrityError: 1062 (23000): Duplicate entry 'U1230' for key 'PRIMARY'


'''


app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="laks;dfjaslk;fjsal;kfjsalfja;lskdfj",
    WTF_CSRF_SECRET_KEY="ofhuio2h3r283ubrqlb32iuob4ir"
))



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.user_loader(lambda id: User.from_id(id, type='student' if id.startswith('U') else 'company'))


@app.context_processor
def add_global_template_vars():
    notifications = add_notification(current_user.id) if not current_user.is_anonymous else None
    return dict(
        search_form=SearchForm(query=request.args.get('query')), # add search form for every page
        notifications=notifications
    )


def student_login_required(func):
    pass


'''

Page Routes

'''


@app.route('/')
def index():
    return render_template('pages/index.j2')

@app.route('/search')
def search():
    query = request.args.get('search')

    return render_template('pages/search.j2')


@app.route('/student/<user>')
def student(user):
    student_data =  stud(user) # get info for a student
    following = listfollowers_user(user)
    friends = listfriends(user)
    return render_template('pages/student.j2', user=student_data, following=following, friends=friends)


@app.route('/company/<user>')
def company(user):
    company_data = com(user)
    followers = listfollowers_company(user)
    jobs = jobs(user)
    return render_template('pages/company.j2', company=company_data, followers=followers, jobs=jobs)


@app.route('/job/<aid>', methods=['GET', 'POST'])
def job(aid):
    thejob_data = selectjob(aid)
    form = ApplicationForm(request.form)
    if request.method == 'POST' and form.validate() and current_user.is_authenticated:
        status = sendapplication(aid, current_user.id, form.email_phone.data)
    return render_template('pages/job.j2', job=thejob_data, aid=aid, form=form)


@app.route('/notifications')
@login_required
def notifications():
    Noti_data = add_notification(current_user.id)
    return render_template('pages/notification.j2', notifs=Noti_data, user=current_user)


# @app.route('/friends/<user>')
# def friends(user):
#     user_data = user # get user info, check if logged in etc.
#     return render_template('pages/friend-list.html', user=user_data)

# @app.route('/followers/<company>')
# def followers(company):
# 	company_data = get_followers(company)
# 	return render_template('pages/friend-list.html', user=company_data)

# @app.route('/following/<user>')
# def following(user):
#     company_data = listfollowers_user(user)
#     return render_template('pages/following.j2', user=company_data)


# @app.route('/friends/<user>')
# def friends(user):
#     friends_data = listfriends(user)
#     return render_template('pages/friends.j2', user=friends_data)


# @app.route('/follower/<company>')
# def followers(company):
#     company_data = listfollowers_company(company)
#     return render_template('pages/follower.j2', user=company_data)

# @app.route('/jobs/<company>')
# def jobs(company=None):
#     jobs_data = jobs(company)
#     return render_template('pages/job.j2', jobs=jobs_data, company=company)





'''

Asynchronous Methods

'''

@app.route('/notification/<aid>/<sid>/mark_read', methods=['POST'])
@login_required
def mark_read(aid, sid):
    status = read_notification(aid, sid) # mark notification as read
    return jsonify({
        'success': status
    })

@app.route('/company/<user>/follow', methods=['POST'])
@login_required
def follow(user):
    status = follow_com(user, current_user.id) 
    return jsonify({
        'success': status
    })

@app.route('/student/<user>/befriend', methods=['POST'])
@login_required
def friend_request(user):
    status = send_friend_request(current_user.id, user)
    return jsonify({
        'success': status
    })

@app.route('/apply/<aid>/<contact_by>', methods=['POST'])
@login_required
def apply(aid, contact_by):
    status = sendapplication(aid, current_user.id, contact_by)
    return jsonify({
        'success': status
    })


'''

Form Pages

'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.from_form(form)
        print(user)
        if user:
            if user.type == 'company':
                login_user(user, remember=form.remember.data)
                print(current_user)
                return redirect(url_for('company', user=user.username))
            elif user.type == 'student':
                login_user(user, remember=form.remember.data)
                return redirect(url_for('student', user=user.username))
    return render_template('form/login.j2', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.from_form(form)
        if form.act_type.data == 'company':
            companyregister(form.name.data, form.password.data, form.username.data)
            if user:
                login_user(user)
                print('logged in company', user.username)
                return redirect(url_for('company', user=user.username))
        elif form.act_type.data == 'student':
            studentregister(form.name.data, form.password.data, form.username.data)
            # user = User.from_form(form)
            if user:
                login_user(user)
                print('logged in user', user.username)
                return redirect(url_for('student', user=user.username))
    return render_template('form/register.j2', form=form)




@app.route('/student/<user>/update', methods=['GET', 'POST'])
@login_required
def student_update(user):
    student_data = stud(user) # get info for a student
    form = UpdateForm(**student_data)
    if request.method == 'POST' and form.validate():
        print(current_user)
        print('122')
        updateprofile(form.phone.data, form.email.data, current_user.id)
        print(form.phone.data)
        print(form.email.data)
        print('123')
    return render_template('form/student_update.j2', form=form, user=student_data)


@app.route('/post_job/<user>', methods=['GET', 'POST'])
@login_required
def post_job(user):
    form = PostJob(request.form)
    student_data =  stud(user) # get info for a student
    if request.method == 'POST' and form.validate():
        pass #
    return render_template('form/job_posting.j2', form=form, user=student_data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.errorhandler(500)
def internal_error(error):
    return render_template('layouts/error.j2', 
        error_code=500, title='Internal Server Error', 
        message="It's our bad. Sorry! :|"), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('layouts/error.j2', 
        error_code=404, title='Page Not Found', 
        message="I think you're lost. That sucks."), 404



# def postjob():
#     form = PostJob(request.form)
#     # company_data = com_from_id(user) # get info for a student
#     if request.method == 'POST' and form.validate():
#         print(current_user)
#         print('122')
#         postjobs(form.phone.data, form.email.data, current_user)
#         print(form.phone.data)
#         print(form.email.data)
#         print('123')
#     return render_template('form/Updateprofile.j2', form=form, user=company_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
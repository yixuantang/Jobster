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

@login_manager.user_loader
def load_user_from_id(id):
    try:
        return User.from_id(id, type='student' if id.startswith('U') else 'company')
    except:
        return None


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

    return render_template('pages/search.j2', title='Search')

##### You can remove this once the messages query is working. it's just for creating fake messages
from datetime import datetime, timedelta

@app.route('/student/<user>')
def student(user):
    student_data =  stud(user) # get info for a student
    following = listfollowers_user(student_data['sid'])
    friends = listfriends(student_data['sid'])
<<<<<<< HEAD
    applications = listapplications(student_data['sid'])
    print(applications)
    print(student_data)
    print(student_data['sid'])
    print(friends)
    return render_template('pages/student.j2', user=student_data, following=following, friends=friends, applications=applications)
=======

    # messages = [
    #     dict(sid1=current_user.id, sid2=student_data['sid'], mtext='Hi', mdate=datetime.now() - timedelta(minutes=25), mstatus=1),
    #     dict(sid1=student_data['sid'], sid2=current_user.id, mtext='Hello', mdate=datetime.now() - timedelta(minutes=20), mstatus=1),
    #     dict(sid1=current_user.id, sid2=student_data['sid'], mtext='yo', mdate=datetime.now() - timedelta(minutes=15), mstatus=1),
    #     dict(sid1=student_data['sid'], sid2=current_user.id, mtext="you're beautiful", mdate=datetime.now() - timedelta(minutes=10), mstatus=1),
    #     dict(sid1=current_user.id, sid2=student_data['sid'], mtext='thanks man', mdate=datetime.now() - timedelta(minutes=5), mstatus=1),
    #     dict(sid1=student_data['sid'], sid2=current_user.id, mtext='poop', mdate=datetime.now() - timedelta(minutes=2), mstatus=1),
    #     dict(sid1=current_user.id, sid2=student_data['sid'], mtext='lol', mdate=datetime.now() - timedelta(minutes=1), mstatus=1),
    # ]
    messages = getmessages(current_user.id, student_data['sid'])
    print(messages)
    return render_template('pages/student.j2', user=student_data, following=following, friends=friends, messages=messages, title=student_data['sname'])
>>>>>>> 5252f7da75103e06be90fd0d84ce52188fa24f38


@app.route('/company/<user>')
def company(user):
    company_data = com(user)
    followers = listfollowers_company(user)
    jobs = comjobs(company_data['cid'])
    applications_com = listapplications_com(company_data['cid'])
    print(company_data['cname'])
    print('123')
    print(user)
<<<<<<< HEAD
    return render_template('pages/company.j2', company=company_data, followers=followers, jobs=jobs, applications_com = applications_com)
=======
    print(current_user.username)
    return render_template('pages/company.j2', company=company_data, followers=followers, jobs=jobs, title=company_data['cname'])

>>>>>>> 5252f7da75103e06be90fd0d84ce52188fa24f38


@app.route('/job/<aid>', methods=['GET', 'POST'])
def job(aid):
    job_data = selectjob(aid)
    form = ApplicationForm(request.form)
    if request.method == 'POST' and form.validate() and current_user.is_authenticated:
        sendapplication(aid, current_user.id, form.email_phone.data)
<<<<<<< HEAD
        return redirect(url_for('student', user=current_user.username))
    return render_template('pages/job.j2', job=job_data, aid=aid, form=form, title=job_data['title'])
=======
        return redirect(url_for('student_edit', user=current_user.username))
    return render_template('pages/job.j2', job=thejob_data, aid=aid, form=form, title=job_data['title'])
>>>>>>> 5252f7da75103e06be90fd0d84ce52188fa24f38


@app.route('/notifications')
@login_required
def notifications():
    Noti_data = add_notification(current_user.id)
    return render_template('pages/notification.j2', notifs=Noti_data, user=current_user, title='Notifications')




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


@app.route('/message/<sid>/send', methods=['POST'])
@login_required
def send_message(sid):
    status = False
    timestamp = datetime.now()
    message = request.form.get('message')

    if message:
        status = sendmessage(current_user.id, sid, message, timestamp)
        sendmessage(sid, current_user.id, 'cool', datetime.now())
    return jsonify({
        'success': status
    })

@app.route('/messages/<sid>/get')
@login_required
def get_messages(sid):
    date = request.args.get('date')
    messages = getnewmessages(sid, current_user.id, date)
    return jsonify({
        # 'success': status,
        'messages': messages
    })

@app.route('/messages/<sid>/all')
@login_required
def get_all_messages(sid):
    messages = getmessages(sid, current_user.id)
    return jsonify({
        # 'success': status,
        'messages': messages
    })


@app.route('/message/<sid>/read/<date>', methods=['POST'])
@login_required
def read_message(sid, date):
    status = markreadmessage(current_user.id, sid, date)
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
    return render_template('form/login.j2', form=form, title='Login')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
<<<<<<< HEAD
        #user = User.from_form(form)
=======
>>>>>>> 5252f7da75103e06be90fd0d84ce52188fa24f38
        if form.act_type.data == 'company':
            companyregister(form.name.data, form.password.data, form.username.data)
            user = User.from_form(form)
            if user:
                login_user(user)
                print('logged in company', user.username)
                return redirect(url_for('company', user=user.username))
        elif form.act_type.data == 'student':
            studentregister(form.name.data, form.password.data, form.username.data)
            user = User.from_form(form)
            if user:
                login_user(user)
                print('logged in user', user.username)
                return redirect(url_for('student', user=user.username))
<<<<<<< HEAD
    return render_template('form/register.j2', form=form, title = 'Register')


# @app.route('/student/<user>/update', methods=['GET', 'POST'])
# @login_required
# def student_update(user):
#      # get info for a student
#     form = UpdateForm(request.form)
#     student_data = stud(user)
#     if request.method == 'POST' and form.validate():
#         print(current_user)
#         print('122')
#         updateprofile(form.phone.data, form.email.data, current_user)
#         print(form.phone.data)
#         print(form.email.data)
#         print('123')
#     return render_template('form/student_update.j2', form=form, user=student_data)

@app.route('/updateprofile/<user>', methods=['GET', 'POST'])
=======
    return render_template('form/register.j2', form=form, title='Register')




@app.route('/student/<user>/edit', methods=['GET', 'POST'])
>>>>>>> 5252f7da75103e06be90fd0d84ce52188fa24f38
@login_required
def student_update(user):
    form = UpdateForm(request.form)
    student_data = stud(user) #use loginname
    print(current_user.id)
    if request.method == 'POST' and form.validate():
        print('123')
        updateprofile(form.phone.data, form.email.data, current_user.id)
        print(current_user.id)
        print(form.email.data)
<<<<<<< HEAD
    return render_template('form/student_update.j2', form=form, user=student_data)
=======
        print('123')
    return render_template('form/Updateprofile.j2', form=form, user=student_data, title='{}|Update Profile'.format(student_data['sname']))

>>>>>>> 5252f7da75103e06be90fd0d84ce52188fa24f38

#func: updateprofile_com
@app.route('/updateprofile_com/<user>', methods=['GET', 'POST'])
@login_required
def company_edit(user):
    form = UpdateForm_com(request.form)
    company_data = com(user) #use loginname
    print(current_user.id)
    if request.method == 'POST' and form.validate():
        print('123')
        updateprofile_com(form.location.data, form.industry.data, current_user.id)
        print(current_user.id)
        print(form.location.data)
    return render_template('form/company_update.j2', form=form, user=company_data)


@app.route('/post_job/<user>', methods=['GET', 'POST'])
@login_required
def post_job(user):
    form = PostJob(request.form)
    company_data = com_from_id(user) # get info for a company
    if request.method == 'POST' and form.validate():
        postjobs(current_user.id,form.joblocation.data,form.title.data,form.salary.data, form.bk.data, form.description.data)
        return redirect(url_for('company', user=company_data['username']))
        print(company_data['location'])
    return render_template('form/job_posting.j2', form=form, company=company_data)

@app.route('/candidate/<user>')
def candidate(user):
    candidate_data =  stud(user) # get info for a student
    following = listfollowers_user(candidate_data['sid'])
    friends = listfriends(candidate_data['sid'])
    applications = listapplications(candidate_data['sid'])
    print(applications)
    print(candidate_data)
    print(candidate_data['sid'])
    print(friends)
    return render_template('pages/candidate.j2', user=candidate_data, following=following, friends=friends, applications=applications)



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
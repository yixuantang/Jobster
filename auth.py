from flask_login import UserMixin
from functions import _student_from_id, _com_from_id, _veristudentpassword, _vericompanypassword



class User(UserMixin):
    def __init__(self, id, name=None, type='student', username=None):
        self.id = id
        self.name = name
        self.type = type
        self.username = username

    @staticmethod
    def from_form(form):
        return User.verify_user_data(username=form.username.data, password=form.password.data, type=form.act_type.data)

    @staticmethod
    def verify_user_data(username, password, type='student'):
        if type == 'company':
            profile_data = _vericompanypassword(username, password)
            return User.from_company_data(profile_data)

        elif type == 'student':
            profile_data = _veristudentpassword(username, password)
            return User.from_student_data(profile_data)
        return None

    @staticmethod
    def from_id(id, type='student'):
        if type == 'student':
            data = _student_from_id(id)
            return User.from_student_data(data)
        elif type == 'company':
            data = _com_from_id(id)
            return User.from_company_data(data)

    @staticmethod
    def from_company_data(data):
        if data:
            return User(data['cid'], data['cname'], 'company', username=data['cname'])
        else:
            return None

    @staticmethod
    def from_student_data(data):
        if data:
            return User(data['sid'], data['sname'], 'student', username=data['loginname'])
        else:
            return None

    def __repr__(self):
        return '<User {}>'.format(self.get_id())











import mysql.connector
import hashlib, uuid
#connection
cnx = mysql.connector.connect(user='root', passwd='root',
                              host='localhost',port='3306',db='love',autocommit=True)
from mysql.connector.cursor import MySQLCursorPrepared
# cursor = cnx.cursor(cursor_class= MySQLCursorPrepared)
cur = cnx.cursor(dictionary=True)

"""
functions
"""

#Com page
def _com(cname):
    cur.execute("select * from company where cname = %s;", (cname,))
    return(cur.fetchone())

def _com_from_id(cid):
    cur.execute("select * from company where cid = %s;", (cid,))
    return(cur.fetchone())

#df student
def _student(loginname):
    cur.execute("select * from student where loginname = %s;", (loginname,))
    return(cur.fetchone())

def _student_from_id(sid):
    cur.execute("select * from student where sid = %s;", (sid,))
    return(cur.fetchone())

#follower
# def _listfollowers_company(x):
#     cur.execute("select s.sname, f.sid from follower f join student s where f.sid = s.sid and cid = '"+x+ "';")
#     followers = cur.fetchall()
#     for f in followers:
#         print(f)

def _listfollowers_company(cid):
    try:
        cur.execute(
            "select s.loginname, s.sname, f.sid from Follower f join Student s where f.sid = s.sid and cid = %s;", (cid,))
        return(cur.fetchall())
    finally:
        pass

#jobs #df
def _jobs(cid):
    cur.execute("select distinct p.*,cname from position p join company c on p.cid = c.cid where p.cid = %s", (cid,))
    return(cur.fetchall())


def student_profile(user):
	student_data = _student(user) # get jobs for a company
	return student_data

#veri passwd
def _veristudentpassword(loginname, passwd):
    cur.execute("select * from student where loginname = %s and password = %s", (loginname, passwd))
    return(cur.fetchone())

def _vericompanypassword(loginname, passwd):
    cur.execute("select * from company where cname = %s and password = %s", (loginname, passwd))
    return(cur.fetchone())

#register
# def _studentregister(sname, password, loginname):
#     cur.execute("INSERT INTO Student(sname, password, loginname) VALUES (%s, %s, %s);",(sname, password, loginname))
#     cur.execute("COMMIT;")

#Notis
def _Notifications(sid):
    cur.execute("select p.*, n.sid, n.ndate, n.nstatus from Notification n join position p on n.aid = p.aid where sid = %s;", (sid,))
    return(cur.fetchall())

#details of job
def _selectjob(aid):
    cur.execute("select p.*, c.cname from company c join position p where c.cid = p.cid and aid = %s;", (aid,))
    return(cur.fetchone())

#regis student
def _studentregister(sname, password, loginname):
    try:
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        cur.execute( "INSERT INTO Student(sname, password, loginname) VALUES (%s, %s, %s);",(sname, hashed_password, loginname))
        cur.execute("COMMIT;")

    finally:
        pass
#regis com
def _companyregister(username, password, cname):
    try:
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        cur.execute( "INSERT INTO Company(username, password, cname) VALUES (%s, %s, %s);",(username, hashed_password, cname))
        cur.execute("COMMIT;")

    finally:
        pass

#update profile
def _studentinfo(sid, sname, loginname, phone, email, university, major, GPA, interests, qualifications, privacysetting, Resume):
    try:
        # salt = uuid.uuid4().hex
        # hashed_password = hashlib.sha512(password + salt).hexdigest()
        cur.execute("""set sql_safe_updates= 0; UPDATE Student 
            set phone = %s, email = %s, university = %s, major = %s, GPA = %s, interests = %s, 
            qualifications = %s, privacy setting = %s, Resume = %s where loginname = %s;""",
        (phone, email, university, major, GPA, interests, qualifications, privacysetting, Resume, loginname))
        cur.execute("COMMIT;")

    finally:
        pass


def updateprofile(phone,email,sid):
    cur.execute("set sql_safe_updates = 0;UPDATE Student set phone = %s, email = %s where sid = %s;", (phone, email, sid), multi=True)
    cnx.commit()

def _listfollowers_user(sid):
    try:
        cur.execute("select f.cid, c.cname from company c join Follower f join Student s where c.cid = f.cid and f.sid = s.sid and s.sid = %s;", (sid,))
        return(cur.fetchall())
    finally:
        pass

#hash password
def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return hashed_password


#list friends
def _listfriends(sid):
    try:
        cur.execute("""select student.loginname, student.sname 
            from (select sid, Friendid from Request where status = 'accepted' and (sid = %s OR Friendid = %s)) as a, 
                student where student.sid != %s and (a.Friendid = student.sid or  a.sid = student.sid);""", (sid, sid, sid))
        return(cur.fetchall())
    finally:
        pass


#application
def _sendapplication(aid, sid, timestamp, contacttype):
    try:
        cur.execute( "INSERT INTO Application(aid, sid, atime, contacttype) VALUES (%s, %s, %s, %s);", (aid, sid, timestamp, contacttype))
        cur.execute("COMMIT;")
        return True
    finally:
        return False

def _postjobs(aid, cid, joblocation,title,salary,bk,description,timestamp):
    try:
        cur.execute( "INSERT INTO position (aid, cid, joblocation,title,salary,bk,description,pdate) VALUES (%s,%s, %s, %s,%s, %s, %s, %s);", (aid, cid, joblocation, title, salary, bk, description, timestamp))
        cur.execute("COMMIT;")
        return True
    finally:
        return False



def _read_notification(aid, sid):
    pass

def _follow_com(cid, sid):
    pass

def _send_friend_request(sid_send, sid_receive):
    pass

def _accept_friend_request(sid_receive, sid_send):
    pass

def _reject_friend_request(sid_receive, sid_send):
    pass


def _search_results(query):
#     cur.execute("""SELECT * from (
#   SELECT 
#     'student' as type, loginname as slug, sname as name, university, major, (MATCH(content) AGAINST (@target)) as relevance
#     from Student WHERE privacysetting LIKE '%public'
#   UNION
#   SELECT 
#     'student' as type, loginname as slug, sname as name, university, major, (MATCH(content) AGAINST (@target)) as relevance
#     from Student WHERE privacysetting LIKE '%public'
#   UNION
#   SELECT 
#     'pages' as 'table_name', 
#     id, 
#     @pages_multiplier * (MATCH(content) AGAINST (@target)) as relevance
#     from pages
# )
# as sitewide WHERE relevance > 0;
# """)
    return(cur.fetchall())







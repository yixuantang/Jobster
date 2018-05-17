import mysql.connector
import hashlib, uuid
from datetime import datetime
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
def com(cname):
    cur.execute("select * from company where cname = %s;", (cname,))
    return(cur.fetchone())

def com_from_id(cid):
    cur.execute("select * from company where cid = %s;", (cid,))
    return(cur.fetchone())

#df student
def stud(loginname):
    cur.execute("select * from student where loginname = %s;", (loginname,))
    return(cur.fetchone())

def student_from_id(sid):
    cur.execute("select * from student where sid = %s;", (sid,))
    return(cur.fetchone())

#follower
# def listfollowers_company(x):
#     cur.execute("select s.sname, f.sid from follower f join student s where f.sid = s.sid and cid = '"+x+ "';")
#     followers = cur.fetchall()
#     for f in followers:
#         print(f)

def listfollowers_company(cid):
    try:
        cur.execute(
            "select s.loginname, s.sname, f.sid from Follower f join Student s where f.sid = s.sid and cid = %s;", (cid,))
        return(cur.fetchall())
    finally:
        pass

#jobs #df
def jobs(cid):
    cur.execute("select distinct p.*,cname from position p join company c on p.cid = c.cid where p.cid = %s", (cid,))
    return(cur.fetchall())


def student_profile(user):
	student_data = _student(user) # get jobs for a company
	return student_data

#veri passwd
def veristudentpassword(loginname, passwd):
    cur.execute("select * from student where loginname = %s and password = %s", (loginname, passwd))
    return(cur.fetchone())

def vericompanypassword(loginname, passwd):
    cur.execute("select * from company where cname = %s and password = %s", (loginname, passwd))
    return(cur.fetchone())

#register
# def studentregister(sname, password, loginname):
#     cur.execute("INSERT INTO Student(sname, password, loginname) VALUES (%s, %s, %s);",(sname, password, loginname))
#     cur.execute("COMMIT;")

#Notis
def add_notification(sid):
    cur.execute("select p.*, n.sid, n.ndate, n.nstatus from Notification n join position p on n.aid = p.aid where sid = %s;", (sid,))
    return(cur.fetchall())

#details of job
def selectjob(aid):
    cur.execute("select p.*, c.cname from company c join position p where c.cid = p.cid and aid = %s;", (aid,))
    return(cur.fetchone())

#regis student
def studentregister(sname, password, loginname):
    try:
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        cur.execute( "INSERT INTO Student(sname, password, loginname) VALUES (%s, %s, %s);",(sname, hashed_password, loginname))
        cur.execute("COMMIT;")

    finally:
        pass
#regis com
def companyregister(username, password, cname):
    try:
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        cur.execute( "INSERT INTO Company(username, password, cname) VALUES (%s, %s, %s);",(username, hashed_password, cname))
        cur.execute("COMMIT;")

    finally:
        pass

#update profile
def studentinfo(sid, sname, loginname, phone, email, university, major, GPA, interests, qualifications, privacysetting, Resume):
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

def listfollowers_user(sid):
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
def listfriends(sid):
    try:
        cur.execute("""select student.loginname, student.sname 
            from (select sid, Friendid from Request where status = 'accepted' and (sid = %s OR Friendid = %s)) as a, 
                student where student.sid != %s and (a.Friendid = student.sid or  a.sid = student.sid);""", (sid, sid, sid))
        return(cur.fetchall())
    finally:
        pass


#application
def sendapplication(aid, sid, contacttype):
    try:
        cur.execute( """INSERT INTO Application(aid, sid, atime, contacttype, astatus) VALUES (%s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE contacttype = %s;""", (aid, sid, datetime.now(), contacttype, 'pending', contacttype))
        cur.execute("COMMIT;")
        return True
    finally:
        pass
    return False

def postjobs(aid, cid, joblocation,title,salary,bk,description,timestamp):
    try:
        cur.execute( "INSERT INTO position (aid, cid, joblocation,title,salary,bk,description,pdate) VALUES (%s,%s, %s, %s,%s, %s, %s, %s);", (aid, cid, joblocation, title, salary, bk, description, timestamp))
        cur.execute("COMMIT;")
        return True
    finally:
        pass
    return False



def read_notification(aid, sid):
    try:
        cur.execute("UPDATE Notification SET nstatus = '1' WHERE aid = %s AND sid = %s;", (aid, sid))
        cur.execute("COMMIT;")
        return True
    finally:
        pass
    return False

def follow_com(cid, sid):
    try:
        cur.execute("INSERT IGNORE INTO Follower (cid, sid, time) VALUES (%s, %s, %s);", (aid, cid, timestamp))
        cur.execute("COMMIT;")
        return True
    finally:
        pass
    return False

def send_friend_request(sid_send, sid_receive):
    try:
        cur.execute("INSERT IGNORE INTO Request (sid,Friendid,status) VALUES (%s,%s,%s);", (sid_send, sid_receive, 0))
        cur.execute("COMMIT;")
        return True
    finally:
        pass
    return False

def accept_friend_request(sid_receive, sid_send):
    try:
        cur.execute("UPDATE Request SET nstatus = '1' WHERE aid = %s AND sid = %s;", (aid, sid))
        cur.execute("COMMIT;")
        return True
    finally:
        pass
    return False

def reject_friend_request(sid_receive, sid_send):
    try:
        cur.execute( "DELETE FROM Request WHERE sid = %s AND Friendid = %s;", (sid_send, sid_receive))
        cur.execute("COMMIT;")
        return True
    finally:
        return False


def search_results(query):
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







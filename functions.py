import mysql.connector
import hashlib, uuid
import MySQLdb
import time
import datetime

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
timeid = datetime.datetime.fromtimestamp(ts).strftime('%m%d%H%M%S')
#connection
#connection
cnx = mysql.connector.connect(user='root', passwd='new_password',
                              host='localhost',port='3306',db='love1',autocommit=True)
from mysql.connector.cursor import MySQLCursorPrepared
# cursor = cnx.cursor(cursor_class= MySQLCursorPrepared)
cur = cnx.cursor(dictionary=True)

"""
functions
"""
salt = 'askjdfhkjashr43iuwq78efbqwuig   7wr83gewguifgiwu3   27eg3e'

#hash password
def hash_password(password):
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return hashed_password

#Com page
def _com(cname):
    cur.execute("select * from company where cname = %s;", (cname,))
    return(cur.fetchone())

def _com_from_id(cid):
    cur.execute("select * from company where cid = %s;", (cid,))
    return(cur.fetchone())

#df student  use sid to find the user
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
        hashed_password = hash_password(password)
        cur.execute( "INSERT INTO Student(sid,sname, password, loginname) VALUES (%s,%s, %s, %s);",(int(timeid), sname, hashed_password, loginname))
        cur.execute("COMMIT;")

    finally:
        pass
#regis com
def _companyregister(username, password, cname):
    try:
        hashed_password = hash_password(password)
        cur.execute( "INSERT INTO Company(cid, username, password, cname) VALUES (%s,%s, %s, %s);",(int(ts),username, hashed_password, cname))
        cur.execute("COMMIT;")

    finally:
        pass

#update profile
def _studentinfo(sid, sname, loginname, phone, email, university, major, GPA, interests, qualifications, privacysetting, Resume):
    try:
        # hashed_password = hash_password(password)
        cur.execute("""set sql_safe_updates= 0; UPDATE Student 
            set phone = %s, email = %s, university = %s, major = %s, GPA = %s, interests = %s, 
            qualifications = %s, privacy setting = %s, Resume = %s where loginname = %s;""",
        (phone, email, university, major, GPA, interests, qualifications, privacysetting, Resume, loginname))
        cur.execute("COMMIT;")

    finally:
        pass

# def updateprofile(phone,email,loginname):
#     cursor = cnx.cursor()
#     try:
#         cursor.execute("set sql_safe_updates= 0; UPDATE Student set phone = %s, email = %s where loginname = %s;"%(phone,email,loginname))
#         cursor.execute("COMMIT;")
#     finally:
#         cursor.close()

def updateprofile(phone,email,sid):
    cur.execute("set sql_safe_updates = 0;UPDATE Student set phone = %s, email = %s where sid = %s;", (phone,email,sid),multi=True)
    cnx.commit()

def _listfollowers_user(sid):
    try:
        cur.execute("select f.cid, c.cname from company c join Follower f join Student s where c.cid = f.cid and f.sid = s.sid and s.sid = %s;", (sid,))
        # followers = pd.DataFrame(cursor.fetchall())
        followers = cur.fetchall()
        print(followers)
        # followers.columns = cursor.column_names
        return(followers)

    finally:
        pass




#list friends
# def _listfriends(sid):
#     cursor = cnx.cursor(dictionary = True)
#     try:
#         #cursor.execute("select student.sname from(select sid, Friendid from Request where status = %s and"%('accepted')+ "(sid = %s OR Friendid = %s)"%(sid,sid)+")as a, student where student.sid != %s and"%(sid)+ "(a.Friendid = student.sid or  a.sid = student.sid);"%(sid,sid))
#         cursor.execute("select s.loginname, s.sname from Request r join Student s on r.Friendid = s.sid where r.status = %s and (r.sid= %s or r.Friendid = %s);",('accepted', sid ,sid))
#         friends = cursor.fetchall()
#         print(friends)
#         print(sid)
#         return(friends)
#     finally:
#         cursor.close()

def _listfriends(sid):
    cursor = cnx.cursor(dictionary=True)
    try:
        cursor.execute("select student.loginname, student.sname, student.sid from(select sid, Friendid from Request where status = 'accepted' and (sid = '"+sid+"' OR Friendid ='"+sid+"'))as a,student where student.sid !='"+sid+"' and (a.Friendid = student.sid or  a.sid = student.sid);")
        friends = cursor.fetchall()
        print(friends)
        return(friends)
    finally:
        cursor.close()
# def _listfriends(sid):
#     try:
#         cur.execute("""select student.loginname, student.sname
#             from (select sid, Friendid from Request where status = 'accepted' and (sid = %s OR Friendid = %s)) as a,
#                 student where student.sid != %s and (a.Friendid = student.sid or  a.sid = student.sid);""", (sid, sid, sid))
#         friends = cur.fetchall()
#         return(friends)
#     finally:
#         pass


#application
def _sendapplication(aid, sid, timestamp, contacttype):
    cursor = cnx.cursor()
    try:
        cursor.execute( "INSERT INTO Application(aid, sid, atime, contacttype) VALUES (%s, %s, %s, %s);", (aid, sid, timestamp, contacttype))
        cursor.execute("COMMIT;")
    finally:
        cursor.close()
#post jobs
def _postjobs(aid, cid, joblocation,title,salary,bk,description,timestamp):
    cursor = cnx.cursor()
    try:
        cursor.execute( "INSERT INTO position (aid, cid, joblocation,title,salary,bk,description,pdate) VALUES (%s,%s, %s, %s,%s, %s, %s, %s);", (aid,cid, joblocation,title,salary,bk,description, timestamp))
        cursor.execute("COMMIT;")
    finally:
        cursor.close()



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







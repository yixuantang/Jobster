#!pip install mysqlclient

import MySQLdb as sql
import hashlib, uuid


cnx = sql.connect(user="root", password = "new_password", host = "localhost", database= "Job_CreateDb")


# Com page
def _com(cid):
    cursor = cnx.cursor(dictionary = True)
    try:
        cursor.execute("select * from company where cid = '%s';" %cid)
        # company = pd.DataFrame(cursor.fetchone())
        company = cursor.fetchone()
        # company.columns = cursor.column_names
        return(company)

    finally:
        cursor.close()

#df student
def _student(loginname):
    cursor = cnx.cursor(dictionary = True)
    try:
        cursor.execute("select * from student where loginname= '%s';" %loginname)
        # student = pd.DataFrame(cursor.fetchone())
        student = cursor.fetchone()
        # student.columns = cursor.column_names
        return(student)

    finally:
        cursor.close()

#list the followers of a company
def _listfollowers_user(cid):   
    cursor = cnx.cursor(dictionary = True)
    try:
        cursor.execute("select s.sname, f.sid from Follower f join Student s where f.sid = s.sid and f.cid ='%s';" %cid)
        # followers = pd.DataFrame(cursor.fetchall())
        followers = cursor.fetchall()
        # followers.columns = cursor.column_names
        return(followers)

    finally:
        cursor.close()


#list the friends
# def _listfriends(rstatus, sid):
#     cursor = cnx.cursor(dictionary = True)
#     try:
#         cursor.execute("select s.sname from Request r join Student s on r.Friendid = s.sid where r.rstatus = %s and (r.sid= %s or r.Friendid = %s);", (rstatus, sid ,sid))
#         friends = cursor.fetchall()

#         return(friends)
#     finally:
#         cursor.close()

def _listfriends(status, sid):
    cursor = cnx.cursor(dictionary)
    try:
        sql_query = '''
        select student.sname from
        (
        select sid, Friendid from Request
        where status = %s and (sid = %s OR Friendid = %s)
        ) as a,
        student
        where student.sid != %s and (a.Friendid = student.sid or a.sid = student.sid); 
        '''
        cursor.execute(sql_query, (status, sid ,sid, sid))
        friends = cursor.fetchall()

        return(friends)
    finally:
        cursor.close()

#list the companies followed by a uer
def _listfollowers_company(sid):
    cursor = cnx.cursor(dictionary = True)
    try:
        cursor.execute("select f.cid, c.cname from Follower f join Company c where f.cid = c.cid and sid ='%s';" %sid)
        # followers_users = pd.DataFrame(cursor.fetchall())
        followers_users = cursor.fetchall()
        # followers_users.columns = cursor.column_names
        return(followers_users)

    finally:
        cursor.close()

def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return hashed_password

    

#student registration function
def _studentregister(sid, sname, password, loginname):
    cursor = cnx.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute( "INSERT INTO Student(sid, sname, password, loginname) VALUES (%s, %s, %s, %s);",(sid, sname, hashed_password, loginname))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()

#company registeration function
def _companyregister(cid, password, cname):
    cursor = cnx.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute( "INSERT INTO Company(cid, password, cname) VALUES (%s, %s, %s);",(cid, hashed_password, cname))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()


#clist the jobs offered by a company
def _jobsoffered(cid):
    cursor = cnx.cursor(dictionary = True)
    try:
        cursor.execute("select distinct p.*,cname from position p join company c on p.cid = c.cid where p.cid = '%s';" %cid)
        # list_jobs= pd.DataFrame(cursor.fetchall())
        list_jobs = cursor.fetchall()
        # list_jobs.columns = cursor.column_names
        return(list_jobs)

    finally:
        cursor.close()

#search keyword function

def _search_company(keyword):
    cursor = cnx.cursor(dictionary = True)
    try:
        cursor.execute("select  p.title, p.description from Company c join position p  where p.cid = c.cid and (p.title like %s or c.cname like %s  or p.description like %s);", (('%' + keyword + '%'), ('%' + keyword + '%'), ('%' + keyword + '%')))

        search_list = cursor.fetchall()
        return(search_list)

    finally:
        cursor.close()

def _search_student(keyword):
    cursor = cnx.cursor(dictionary = True)
    try:
        cursor.execute("select s.sname, s.sid from Student s where (s.sname like %s or s.interests like %s  or s.qualifications like %s or s.major like %s or s.university like %s);", (('%' + keyword + '%'), ('%' + keyword + '%'), ('%' + keyword + '%'), ('%' + keyword + '%'), ('%' + keyword + '%')))

        search_list = cursor.fetchall()
        return(search_list)

    finally:
        cursor.close()




# def _search(title, description):
#     cursor = cnx.cursor(dictionary = True)
#     try:
#         cursor.execute("select p.title, p.description from Company c join position p where p.title like %s or p.description like %s;",(title, description))
#         # search_list= pd.DataFrame(cursor.fetchall())
#         search_list = cursor.fetchall()
#         # search_list.columns = curson.column_names
#         return(search_list)

#     finally:
        # cursor.close()

#send messages to a friend
def _sendmessage(sid1, sid2, mtext, mdate):
    cursor = cnx.cursor()
    try:
        cursor.execute( "INSERT INTO Message(sid1, sid2, mtext, mdate) VALUES (%s, %s, %s, %s);",(sid1, sid2, mtext, mdate))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()

#send notifications
def _sendnotification(aid, sid, ndate):
    cursor = cnx.cursor()
    try:
        cursor.execute( "INSERT INTO Notification(aid, sid, ndate) VALUES (%s, %s, %s);", (aid, sid, ndate))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()
        
# def student_profile(user):
#     student_data = _student(user) # get jobs for a company
#     return student_data

#insert announcements
def _postjobs(aid,cid,joblocation,title,salary,bk,description,pdate):
    cursor = cnx.cursor()
    try:
        cursor.execute("INSERT INTO position(aid, cid, joblocation, title, salary, bk, description, pdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",(aid, cid, joblocation, title, salary, bk, description, pdate))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()

#student info page

def _studentinfo(loginname, phone, email, university, major, GPA, interests, qualifications, privacysetting, Resume):
    cursor = cnx.cursor()
    try:
        # salt = uuid.uuid4().hex
        # hashed_password = hashlib.sha512(password + salt).hexdigest()
        cursor.execute("set sql_safe_updates= 0; UPDATE Student set phone = %s, email = %s, university = %s, major = %s, GPA = %s, interests = %s, qualifications = %s, privacysetting = %s, Resume = %s where loginname = %s;",
        (phone, email, university, major, GPA, interests, qualifications, privacysetting, Resume, loginname))
        
        cursor.execute("COMMIT;")
    finally:
        cursor.close()

#add a friend
def _addfriend(sid, Friendid, rstatus, rdate, answer_date):
    cursor = cnx.cursor()
    try:
        cursor.execute("INSERT INTO Request(sid, Friendid, rstatus, rdate, answer_date) VALUES (%s, %s, %s, %s, %s);",(sid, Friendid, rstatus, rdate, answer_date))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()


#update a friend request status
def _updatefriendstatus(sid, Friendid, rstatus, answer_date ):
    cursor = cnx.cursor()
    try:
        cursor.execute("set sql_safe_updates= 0; UPDATE Request set rstatus = %s, answer_date = %s where sid = %s and Friendid = %s",(rstatus, answer_date, sid, Friendid))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()


#add a follower
def _addfollower(cid, sid, ftime):
    cursor = cnx.cursor()
    try:
        cursor.execute("INSERT INTO Follower(cid, sid, ftime) VALUES (%s, %s, %s, %s, %s);",(cid, sid, ftime))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()    

#delete the follower
def _updatefollower(cid, sid):
    cursor = cnx.cursor()
    try:
        cursor.execute("delete from Follower where cid = %s and sid = %s;",(cid, sid))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()

#insert into application
def _sendapplication(aid, sid, atime, contacttype, astatus):
    cursor = cnx.cursor()
    try:
        cursor.execute( "INSERT INTO Application(aid, sid, atime, contacttype, astatus) VALUES (%s, %s, %s, %s, %s);", (aid, sid, atime, contacttype, astatus))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()
        
#count the total number
# def _countnotification_message()


def _countnotifimessage():
    cursor = cnx.cursor()
    sql_query = '''
    select  count(aid) from Notification where nstatus = %s
    UNION ALL
    select count(mtext) from Message where mstatus = %s;
    '''
    try:
        cursor.execute( sql_query, (0, 0))
        cursor.execute("COMMIT;")

    finally:
        cursor.close()

# def _notify(keyword):
#     student_names = dict(_search_student(keyword))
    
#notify students after searching them 
def _notify(keyword, aid, ndate):
    student_names = list(_search_student(keyword))
    for i in student_names:
        _sendnotification(aid, i["sid"], ndate)
        









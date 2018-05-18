
#design the job web databse
DROP TABLE IF EXISTS `Student`;
CREATE TABLE `Student` (
  `sid` VARCHAR(20) NOT NULL,
  `sname` VARCHAR(20) NOT NULL,
  `password` VARCHAR(1000) NOT NULL, 
  `loginname` VARCHAR(20) NOT NULL,
  `phone` VARCHAR(10) ,
  `email` VARCHAR(45) ,
  `university` VARCHAR(40) ,
  `major` VARCHAR(15) ,
  `GPA` VARCHAR(10) ,
  `interests` VARCHAR(40) ,
  `qualifications` VARCHAR(30),
  `privacysetting` VARCHAR(30) default 'public',
  `Resume` LONGBLOB ,
  UNIQUE (`sid`),
  UNIQUE(`loginname`),
  UNIQUE(`email`),
  UNIQUE(`phone`),
  PRIMARY KEY (`sid`));

--   
INSERT INTO `Student` VALUES ('U1245', 'Joan Arc', 'MarkTwain','Joan','5535','joan@nyu.edu','NYU','CS','3.34','playing games','BS in Computer Science','public','database systems, computer science');
INSERT INTO `Student` VALUES ('U4785','Isha Chaturvedi', 'Joshua','Isha Chaturvedi','5353','ic1018@nyu.edu','NYU','CS','3.5','dancing','MS in Data Science','public','database systems, algorithms, data science, machine learing');
INSERT INTO `Student` VALUES ('U7234', 'Yixuan Tang', 'Dorling','Tang','5674','yt41@stanford.edu','Stanford','CS','3.9','singing','MS in Urban Data Science','public','database systems, data science, mobility, machine learning');
INSERT INTO `Student` VALUES ('U2384', 'Gaurav Bhardwaj', 'FrenchD','Gaurav Bhardwaj','5327','gb242@nyu.edu','NYU','CS','3.3','soccer','BS in Electronics','friendly public','telecommunications, computer networks, embedded systems');
INSERT INTO `Student` VALUES ('U3984', 'Charles Moffett', 'CharlesS','Charles Moffett','5273','cm6353@columbia.edu','Columbia','Marketting','3.9','soccer','MS in Marketting','public','global markets, markets and design, rapid prototyping');
INSERT INTO  `Student` VALUES('U1246', 'Yu Chen', 'sql2018','Yu','5270','YU@fordham.edu','Fordham','EE','3.9','soccer','MS in Marketting','friendly public','global markets, programming');
-- 

DROP TABLE IF EXISTS `Company`;
CREATE TABLE `Company` (
  `cid` VARCHAR(20) NOT NULL,
  `username` VARCHAR(20) NOT NULL,
  `password` VARCHAR(1000) NOT NULL,
  `cname` VARCHAR(20) NOT NULL,
  `location` VARCHAR(30) ,
  `industry` VARCHAR(45) ,
  UNIQUE (`cid`),
  UNIQUE(`cname`),
  PRIMARY KEY (`cid`));

  
INSERT INTO `Company` VALUES ('C1245','Google', 'db2016','Google', 'Mt View','Technology');
INSERT INTO `Company` VALUES ('C4785', 'Apple','jobs111','Apple','Cupertino','Technology');
INSERT INTO `Company` VALUES ('C7234','Mic', 'Mic2008','Microsoft','Washington','Technology');
INSERT INTO `Company` VALUES ('C2384','Yahoo', 'Yahoo2','Yahoo','Sunntvale','Webservices');
INSERT INTO `Company` VALUES ('C3984', 'Facebook','cc2009','Facebook','Menlo Park','Social Media');

DROP TABLE IF EXISTS `position`;
CREATE TABLE `position` (
  `aid` VARCHAR(10) NOT NULL,
  `cid` VARCHAR(10) NOT NULL,
  `joblocation` VARCHAR(10) NOT NULL,
  `title` VARCHAR(25) NOT NULL,
  `salary` VARCHAR(20) NOT NULL,
  `bk` VARCHAR(30) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `pdate` DATETIME NOT NULL,
  UNIQUE (`aid`),
  PRIMARY KEY (`aid`),
  FOREIGN KEY (`cid`) REFERENCES `Company` (`cid`));  


INSERT INTO `position` VALUES ('A1245', 'C1245', 'Mt View','Developer','80000', 'BS in Computer Science','Application Development','2017-02-20 08:06:13');
INSERT INTO `position` VALUES ('A4785', 'C4785','Cupertino','Software Engineer','90000','BS in Computer Science','Debugging, Testing','2017-06-20 08:06:13');
INSERT INTO `position` VALUES ('A7234', 'C7234', 'Washington','Data Scientist','100000','Masters in Data Science','Gesture Recognition','2017-08-20 08:06:13');
INSERT INTO `position` VALUES ('A2384', 'C2384', 'Sunnyvale','Data Engineer','75000','Masters in Data Science','Create API','2017-12-20 08:06:13');
INSERT INTO `position` VALUES ('A3984', 'C3984', 'Menlo Park','UX Writer','65000','BS in any field','Writing Story','2018-02-20 18:06:13');
INSERT INTO `position` VALUES ('A3985', 'C3984', 'Menlo Park','UI developer','65000','MS in Computer Science','Front-end developer','2018-04-19 08:26:13');
  
  
DROP TABLE IF EXISTS `Follower`;
CREATE TABLE `Follower` (
  `cid` VARCHAR(10) NOT NULL,
  `sid` VARCHAR(10) NOT NULL,
  `time` DATETIME NOT NULL,

  PRIMARY KEY (`cid`,`sid`),
  FOREIGN KEY (`cid`) REFERENCES `Company` (`cid`),
  FOREIGN KEY (`sid`) REFERENCES `Student` (`sid`));  
-- --   

INSERT INTO `Follower` VALUES ('C8559', 'U8543','2018-05-16 10:12:10');

INSERT INTO `Follower` VALUES ('C1253', 'U1523', now());
INSERT INTO `Follower` VALUES ('C1253', 'U6252', now());
--
INSERT INTO `Follower` VALUES ('C1245', 'U1245','2017-10-20 08:16:10');
INSERT INTO `Follower` VALUES ('C4785', 'U4785','2017-10-20 08:12:10');
INSERT INTO `Follower` VALUES ('C2384', 'U7234','2017-12-20 08:16:10');
INSERT INTO `Follower` VALUES ('C2384', 'U4785','2018-01-20 08:16:10');
INSERT INTO `Follower` VALUES ('C3984', 'U1245','2017-10-15 08:16:10');
INSERT INTO `Follower` VALUES ('C7234', 'U1245','2017-10-20 22:16:10');

DROP TABLE IF EXISTS `Request`;
CREATE TABLE `Request` (
  `sid` VARCHAR(10) NOT NULL,
  `Friendid` VARCHAR(10) NOT NULL,
  `status` VARCHAR(10) NOT NULL default 'pending',
  `rdate` DATETIME NOT NULL,
  `answer_date` DATETIME,
  PRIMARY KEY (`sid`,  `Friendid`),
  constraint CK_T1 CHECK (sid < Friendid),
  constraint UQ_T1 UNIQUE (sid,Friendid),
--   UNIQUE(`sid`,`Friendid`),
  FOREIGN KEY (`sid`) REFERENCES `Student` (`sid`),
  FOREIGN KEY (`Friendid`) REFERENCES `Student` (`sid`));

INSERT INTO `Request`(`sid`,`Friendid`,`rdate`) VALUES ('U2556','U6002','2018-05-17 11:59:19');
INSERT INTO `Request`(`sid`,`Friendid`,`rdate`) VALUES ('U2556','U6002','2018-05-17 11:59:19');

INSERT INTO `Request` VALUES ('U6002','U9268','accepted','2018-05-17 11:00:00', '2018-05-17 11:00:00');
INSERT INTO `Request` VALUES ('U2556','U9268','pending','2018-05-17 11:58:00');
INSERT INTO `Request`(`sid`,`Friendid`,`rdate`) VALUES ('U2556','U6002','2018-05-17 11:59:19');

INSERT INTO `Request` VALUES ('U2556','U1523','accepted','2018-05-17 11:39:19', '2018-05-17 11:39:40');
INSERT INTO `Request` VALUES ('U6002','U8543','accepted','2018-05-17 04:29:10', '2018-05-17 04:29:56');
INSERT INTO `Request` VALUES ('U4785','U2384','rejected','2017-11-20 08:06:10', '2017-11-20 18:06:10');
INSERT INTO `Request` VALUES ('U7234','U1245','pending','2017-12-20 08:06:10', null );
INSERT INTO `Request` VALUES ('U4785','U7234','accepted','2018-02-20 08:26:10', '2018-03-20 08:26:10');
INSERT INTO `Request` VALUES ('U1245','U2384','pending','2018-03-20 08:26:12', null);
INSERT INTO `Request` VALUES('U1246','U1245', 'accepted', '2018-04-01 11:26:10', '2018-04-02 11:26:10');
INSERT INTO `Request` VALUES('U3984','U1246', 'pending', '2018-01-15', null);

DROP TABLE IF EXISTS `Message`;
CREATE TABLE `Message` (
  `sid1` VARCHAR(10) NOT NULL,
  `sid2` VARCHAR(10) NOT NULL,
  `mtext` VARCHAR(100) NOT NULL,
  `mdate` DATETIME NOT NULL,
  `mstatus` integer(10) DEFAULT '0',

  PRIMARY KEY (`sid1`,`sid2`,`mdate`),
  FOREIGN KEY (`sid1`) REFERENCES `Student` (`sid`),
  FOREIGN KEY (`sid2`) REFERENCES `Student` (`sid`));
  

INSERT INTO `Message` VALUES ('U1245','U4785','hi','2017-10-20 08:06:10','1');
INSERT INTO `Message` VALUES ('U4785','U1245','hello','2017-11-20 09:06:10','1');
INSERT INTO `Message` VALUES ('U7234','U4785','your profile is good ','2017-12-20 10:06:10','1');
INSERT INTO `Message` VALUES ('U4785','U7234','thanks','2018-02-20 11:06:10','1');
INSERT INTO `Message` VALUES ('U1245','U4785','how is it going?','2018-03-20 12:06:10','1');
  

DROP TABLE IF EXISTS `Notification`;
CREATE TABLE `Notification` (
  `aid` VARCHAR(10) NOT NULL,
  `sid` VARCHAR(10) NOT NULL,
  `ndate` DATETIME NOT NULL,
  `nstatus` integer(10) DEFAULT '0',
  PRIMARY KEY (`aid`,`sid`,`ndate`),
  FOREIGN KEY (`aid`) REFERENCES `position` (`aid`),
  FOREIGN KEY (`sid`) REFERENCES `Student` (`sid`));
  
  
INSERT INTO `Notification` VALUES ('A1245','U1245','2017-10-20 08:06:13','0');
INSERT INTO `Notification` VALUES ('A4785','U4785','2017-11-20 08:22:13','0');
INSERT INTO `Notification` VALUES ('A7234','U7234','2017-12-20 18:06:13','0');
INSERT INTO `Notification` VALUES ('A3984','U4785','2018-02-20 22:06:22','1');
INSERT INTO `Notification` VALUES ('A1245','U1246','2018-03-20 08:16:13','1');


DROP TABLE IF EXISTS `Application`;
CREATE TABLE `Application` (
  `aid` VARCHAR(10) NOT NULL,
  `sid` VARCHAR(10) NOT NULL,
  `atime` DATETIME NOT NULL,
  `contacttype` VARCHAR(30) NOT NULL,
  `astatus` VARCHAR(10) NOT NULL default 'pending',
  UNIQUE(`aid`,`sid`),
  PRIMARY KEY (`aid`,`sid`),
  FOREIGN KEY (`aid`) REFERENCES `position` (`aid`),
  FOREIGN KEY (`sid`) REFERENCES `Student` (`sid`));
-- 
INSERT INTO `Application` VALUES ('A8599','U8543','2018-05-17 01:06:13','email', 'success');
INSERT INTO `Application` VALUES ('A8599','U8734','2018-05-17 01:06:13','email', 'pending');

INSERT INTO `Application` VALUES ('A1245','U1245','2017-10-20 08:06:13','email', 'success');
INSERT INTO `Application` VALUES ('A4785','U4785','2017-12-20 09:06:13','phone', 'success');
INSERT INTO `Application` VALUES ('A7234','U7234','2018-01-20 12:06:13','phone', 'pending');
INSERT INTO `Application` VALUES ('A3984','U4785','2018-02-20 15:06:13','email', 'success');
INSERT INTO `Application` VALUES ('A2384','U3984','2017-12-10 08:34:13','email', 'pending');
INSERT INTO `Application` VALUES ('A2384','U7234',now(),'123','');
-- 
ALTER TABLE student MODIFY phone VARCHAR(20);
ALTER TABLE student MODIFY resume longblob;
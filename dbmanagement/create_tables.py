import mysql.connector
import environ

env = environ.Env()
environ.Env.read_env()

connection = mysql.connector.connect(
  host=env("MYSQL_HOST"),
  user= env("MYSQL_USER"),
  password= env("MYSQL_PASSWORD"),
  database= env("MYSQL_DB"),
  auth_plugin="mysql_native_password"
)

cursor = connection.cursor()

# cursor.execute("""CREATE TABLE `DBManager` (
#     `manager_id` int NOT NULL AUTO_INCREMENT,
#     `username` varchar(64) UNIQUE,
#     `password` varchar(64),
#     PRIMARY KEY (`manager_id`)
# );""")

# cursor.execute("""CREATE TABLE `Department` (
#     `department_id` varchar(64) NOT NULL,
#     `name` varchar(256) UNIQUE,
#     PRIMARY KEY (`department_id`)
# );""")

# cursor.execute("""CREATE TABLE `Classroom` (
#     `classroom_id` varchar(64) NOT NULL,
#     `campus` varchar(256),
#     `capacity` int,
#     PRIMARY KEY (`classroom_id`)
# );""")

# cursor.execute("""CREATE TABLE `Instructors` (
#     `username` varchar(64) NOT NULL,
#     `name` varchar(256),
#     `surname` varchar(256),
#     `email` varchar(256),
#     `password` varchar(64) NOT NULL,
#     `department_id` varchar(64) NOT NULL,
#     `title` varchar(45) NOT NULL,
#     PRIMARY KEY (`username`),
#     KEY `department_id` (`department_id`),
#     FOREIGN KEY (`department_id`) REFERENCES `Department` (`department_id`) ON DELETE CASCADE,
#     CHECK ((`title` = "Assistant Professor")
#         OR (`title` = "Associate Professor")
#         OR (`title` = "Professor"))
# );""")

# cursor.execute("""CREATE TABLE `Students` (
#     `username` varchar(64) NOT NULL,
#     `name` varchar(256),
#     `surname` varchar(256),
#     `email` varchar(256),
#     `password` varchar(64) NOT NULL,
#     `department_id` varchar(64) NOT NULL,
#     `student_id` int UNIQUE NOT NULL ,
#     `GPA` float(3, 2),
#     `credits` int,
#     PRIMARY KEY (`username`),
#     FOREIGN KEY (`department_id`) REFERENCES `Department` (`department_id`)
# );""")


# cursor.execute("""CREATE TABLE `Course` (
#     `course_id` varchar(64) NOT NULL,
#     `credits` int,
#     `name` varchar(256),
#     `quota` int,
#     `instr_username` varchar(64),
#     PRIMARY KEY (`course_id`),
#     FOREIGN KEY (`instr_username`) REFERENCES Instructors(`username`) ON DELETE CASCADE
# );""")

# connection.commit()


# cursor.execute("""CREATE TABLE `Given_At` (
#     `course_id` varchar(64) NOT NULL,
#     `classroom_id` varchar(64) NOT NULL,
#     `time_slot` int NOT NULL,
#     PRIMARY KEY (`course_id`, `classroom_id`),
#     UNIQUE (`classroom_id`, `time_slot`),
#     FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`) ON DELETE CASCADE,
#     FOREIGN KEY (`classroom_id`) REFERENCES `Classroom` (`classroom_id`) ON DELETE CASCADE
# );""")

# cursor.execute("""CREATE TABLE `Has_Grade` (
#     `student_username` varchar(64) NOT NULL,
#     `course_id` varchar(64) NOT NULL,
#     `grade` float(2, 1),
#     PRIMARY KEY (`student_username`, `course_id`),
#     FOREIGN KEY (`student_username`) REFERENCES `Students` (`username`) ON DELETE CASCADE,
#     FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`) ON DELETE CASCADE
# );""")

# cursor.execute("""CREATE TABLE `Has_Prerequisite` (
#     `course_id` varchar(64) NOT NULL,
#     `prereq_id` varchar(64) NOT NULL,
#     PRIMARY KEY (`course_id`, `prereq_id`),
#     FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`) ON DELETE CASCADE,
#     FOREIGN KEY (`prereq_id`) REFERENCES `Course` (`course_id`) ON DELETE CASCADE,
#     CHECK (`course_id` > `prereq_id`)
# );""")

# cursor.execute("""CREATE TABLE `Taken` (
#     `username` varchar(64) NOT NULL,
#     `course_id` varchar(64) NOT NULL,
#     PRIMARY KEY (`username`, `course_id`),
#     FOREIGN KEY (`username`) REFERENCES `Students` (`username`) ON DELETE CASCADE,
#     FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`) ON DELETE CASCADE
# );""")

# connection.commit()

cursor.execute("""CREATE TRIGGER `ClassroomCapacityCheck`
AFTER INSERT ON `Given_At` 
FOR EACH ROW 
BEGIN 
    IF (SELECT `quota` FROM Course WHERE `course_id` = NEW.course_id) > (SELECT `capacity` FROM Classroom WHERE NEW.classroom_id = `classroom_id`) THEN
        DELETE FROM Course WHERE Course.`course_id` = NEW.course_id;
    END IF;
END;""")

cursor.execute("""CREATE TRIGGER `RemoveFromTaken` AFTER INSERT ON `Has_Grade` 
FOR EACH ROW 
BEGIN
    DELETE FROM Taken 
    WHERE (`course_id` = NEW.course_id)
        AND (`username` = NEW.student_username);
END;""")

cursor.execute("""CREATE TRIGGER `StudentAutomator` AFTER INSERT ON `Has_Grade` 
FOR EACH ROW 
BEGIN
    UPDATE Students
    SET Students.credits = Students.credits + 
        (SELECT `credits` FROM Course WHERE Course.`course_id` = NEW.course_id),

        Students.GPA = (SELECT SUM(Course.`credits` * `grade`) FROM Has_Grade
                    INNER JOIN Course ON Has_Grade.`course_id` = Course.`course_id`
                    WHERE `student_username` = Students.`username`) / Students.`credits`
    WHERE Students.username = NEW.student_username;
END;""")

cursor.execute("""CREATE TRIGGER `UpdateAfterGrade` AFTER UPDATE ON `Has_Grade` 
FOR EACH ROW 
BEGIN
    UPDATE Students
    SET Students.credits = (SELECT SUM(`credits`) FROM Course
                    INNER JOIN Has_Grade ON Course.`course_id` = Has_Grade.`course_id`
                    WHERE NEW.`student_username` = Has_Grade.`student_username`),
    Students.GPA = (SELECT SUM(Course.`credits` * `grade`) FROM Has_Grade
                INNER JOIN Course ON Has_Grade.`course_id` = Course.`course_id`
                WHERE `student_username` = Students.`username`) / Students.`credits`
    WHERE Students.username = NEW.student_username;
END;""")

cursor.execute("""CREATE TRIGGER `AfterDeleteGrade` AFTER DELETE ON `Has_Grade` 
FOR EACH ROW 
BEGIN
    UPDATE Students
    SET Students.credits = (SELECT SUM(`credits`) FROM Course
                INNER JOIN Has_Grade ON Course.`course_id` = Has_Grade.`course_id`
                WHERE OLD.`student_username` = Has_Grade.`student_username`),
        Students.GPA = (SELECT SUM(Course.`credits` * `grade`) FROM Has_Grade
                INNER JOIN Course ON Has_Grade.`course_id` = Course.`course_id`
                WHERE `student_username` = Students.`username`) / Students.`credits`
    WHERE Students.username = OLD.student_username;
END;""")

cursor.execute("""CREATE TRIGGER `AddCourseCheck` BEFORE INSERT ON `Taken` 
FOR EACH ROW 
BEGIN 
    IF NEW.course_id IN (SELECT `course_id` FROM `Has_Grade` WHERE `student_username` = NEW.username) THEN 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A student can not take a course they have previously taken.';
    END IF;
END;""")

cursor.execute("""CREATE TRIGGER `CheckQuota` BEFORE INSERT ON `Taken` 
FOR EACH ROW 
BEGIN 
    IF (SELECT count(`username`) FROM Taken WHERE `course_id` = NEW.`course_id`) = (SELECT `quota` FROM Course WHERE `course_id` = NEW.`course_id`) THEN 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "Course quota is full.";
    END IF;
END;""")

# Trigger to check course prerequisites on course addition for student
cursor.execute("""
CREATE TRIGGER `CheckPrerequisites` BEFORE INSERT ON `Taken` FOR EACH ROW BEGIN
	DECLARE `prereq_count` INT;
	DECLARE `met_count` INT;
	
	SET `met_count` = (SELECT count(Has_Grade.`course_id`) FROM Has_Grade INNER JOIN Has_Prerequisite ON Has_Grade.`course_id` = Has_Prerequisite.`prereq_id` WHERE Has_Prerequisite.`course_id` = NEW.course_id AND `student_username` = NEW.username);
	
	SET `prereq_count` = (SELECT count(`prereq_id`) FROM Has_Prerequisite WHERE `course_id` = NEW.course_id);
	
	IF `met_count` <> `prereq_count` THEN
		SIGNAL SQLSTATE '45000' 
		SET MESSAGE_TEXT = "Prerequisites for these course is not met.";
	END IF;
END;""")

# Stored procedure to filter courses
cursor.execute("""CREATE PROCEDURE `FilterCourses`(IN dept_id TEXT, IN campus TEXT, IN min_creds INT, IN max_creds INT)
BEGIN
    SELECT Course.`course_id`, Course.`name`, Instructors.`surname`, Instructors.`department_id`, Course.`credits`, Given_At.`classroom_id`, Given_At.`time_slot`, Course.`quota` 
    FROM Course
    INNER JOIN Instructors ON Instructors.`username` = Course.`instr_username`
    INNER JOIN Given_At ON Given_At.`course_id` = Course.`course_id`
    INNER JOIN Classroom ON Classroom.`classroom_id` = Given_At.`classroom_id`
    WHERE (Course.`credits` <= max_creds OR Course.`credits` >= min_creds) AND (Instructors.`department_id` = dept_id) AND (Classroom.`campus` = campus);
END;""")

connection.commit()
import mysql.connector
import environ

env = environ.Env()
environ.Env.read_env()

connection = mysql.connector.connect(
  host="localhost",
  user="django",
  password="c3tg2RB8QzN^zn",
  database="cmpe321",
  auth_plugin='mysql_native_password'
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS DBManager(
    `manager_id` INT  AUTO_INCREMENT,
    `username` VARCHAR(48)  UNIQUE,
    `password` VARCHAR(48),
    PRIMARY KEY(`manager_id`)
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Department(
    `department_id` VARCHAR(48),
    `name` VARCHAR(256)  UNIQUE,
    PRIMARY KEY (`department_id`)
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Instructors(
    `username` VARCHAR(48) NOT NULL,
    `name` VARCHAR(256),
    `surname` VARCHAR(256),
    `email` VARCHAR(256),
    `password` VARCHAR(256) NOT NULL,
    `department_id` VARCHAR(48) NOT NULL,
    `title` VARCHAR(48) NOT NULL,
    PRIMARY KEY(`username`),
    FOREIGN KEY (`department_id`) REFERENCES Department(`department_id`) ON DELETE CASCADE
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Students(
    `username` VARCHAR(48) NOT NULL,
    `name` VARCHAR(256),
    `surname` VARCHAR(256),
    `email` VARCHAR(256),
    `password` VARCHAR(256) NOT NULL,
    `department_id` VARCHAR(48) NOT NULL,
    `student_id` INT UNIQUE NOT NULL,
    `GPA` FLOAT,
    `credits` INT,
    PRIMARY KEY(`username`),
    FOREIGN KEY (`department_id`) REFERENCES Department(`department_id`) ON DELETE CASCADE
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Course(
    `course_id` VARCHAR(48) ,
    `credits` INT,
    `name` VARCHAR(256) ,
    `quota` INT,
    `instr_username` VARCHAR(48),
    PRIMARY KEY (`course_id`),
    FOREIGN KEY (`instr_username`) REFERENCES Instructors(`username`) ON DELETE SET NULL
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Classroom(
    `classroom_id` VARCHAR(48) ,
    `campus` VARCHAR(256),
    `capacity` INT,
    PRIMARY KEY(`classroom_id`)
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Taken(
    `username` VARCHAR(48) ,
    `course_id` VARCHAR(48) ,
    PRIMARY KEY(`username`, `course_id`),
    FOREIGN KEY (`username`) REFERENCES Students(`username`) ON DELETE CASCADE,
    FOREIGN KEY (`course_id`) REFERENCES Course(`course_id`) ON DELETE CASCADE
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Has_Grade(
    `student_username` VARCHAR(48),
    `course_id` VARCHAR(48),
    `grade` FLOAT,
    PRIMARY KEY(`student_username`, `course_id`),
    FOREIGN KEY(`student_username`) REFERENCES Students(`username`) ON DELETE CASCADE,
    FOREIGN KEY(`course_id`) REFERENCES Course(`course_id`) ON DELETE CASCADE
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Has_Prerequisite(
    `course_id` VARCHAR(48),
    `prereq_id` VARCHAR(48),
    PRIMARY KEY(`course_id`, `prereq_id`),
    FOREIGN KEY(`course_id`) REFERENCES Course(`course_id`) ON DELETE CASCADE,
    FOREIGN KEY(`prereq_id`) REFERENCES Course(`course_id`) ON DELETE CASCADE,
    CHECK (`course_id` > `prereq_id`)
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Given_At(
    `course_id` VARCHAR(48) NOT NULL,
    `classroom_id` VARCHAR(48),
    `time_slot` INT NOT NULL UNIQUE,
    PRIMARY KEY(`course_id`, `classroom_id`),
    FOREIGN KEY(`course_id`) REFERENCES Course(`course_id`) ON DELETE CASCADE,
    FOREIGN KEY(`classroom_id`) REFERENCES Classroom(`classroom_id`) ON DELETE CASCADE,
    CHECK (`time_slot` < 11 AND `time_slot` > 0)
);""")

# cursor.execute("""
# CREATE PROCEDURE FilterCourses(IN dept_id TEXT, IN campus TEXT, IN min_creds INT, IN max_creds INT)
# BEGIN
#     SELECT *
#     FROM Course
#     INNER JOIN Instructors ON `Instructors.username` = `Course.instr_username`
#     INNER JOIN Given_At ON `Given_At.course_id` = `Course.course_id`
#     INNER JOIN Classroom ON `Classroom.classroom_id` = `Given_At.classroom_id`
#     WHERE (`Course.credits` <= max_creds OR `Course.credits` >= min_creds) AND (`Instructors.department_id` = dept_id) AND (`Classroom.campus` = campus);
# END;""")

cursor.execute("DROP TRIGGER GradeAutomator;")

cursor.execute("""
CREATE TRIGGER GradeAutomator
AFTER INSERT ON Has_Grade
FOR EACH ROW
BEGIN
    UPDATE Students
    SET Students.credits = `Students.credits` + (SELECT `Course.credits` FROM Course WHERE `Course.course_id` = NEW.course_id),
    Students.GPA = (SELECT SUM(`Has_Grade.grade`) FROM `Has_Grade` WHERE `Has_Grade.student_username` = `Students.username`)/`Students.credits`
    WHERE `Students.username` = NEW.student_username;
END;""")

cursor.execute("DROP TRIGGER IF EXISTS RemoveFromTaken;")

# cursor.execute("""
# CREATE TRIGGER RemoveFromTaken
# AFTER INSERT ON Has_Grade
# FOR EACH ROW
# BEGIN
#     DELETE FROM Taken WHERE (`Taken.course_id` = NEW.course_id) AND (`Taken.username` = NEW.student_username);
# END;""")

cursor.execute("DROP TRIGGER ClassroomAllocation")

cursor.execute("""
CREATE TRIGGER ClassroomAllocation
BEFORE INSERT ON Given_At
FOR EACH ROW
BEGIN
    IF (SELECT `quota` FROM Course WHERE `course_id` = NEW.course_id) > (SELECT `capacity` FROM Classroom WHERE NEW.classroom_id = `classroom_id`) THEN 
        DELETE FROM Course WHERE `course_id` = NEW.course_id;
        SIGNAL SQLSTATE '45000';
    END IF;
END;""")


cursor.execute("DROP TRIGGER AddCourseCheck;")
cursor.execute("""
CREATE TRIGGER AddCourseCheck
BEFORE INSERT ON Taken
FOR EACH ROW
BEGIN
    IF NEW.course_id IN (SELECT `course_id` FROM `Has_Grade` WHERE `student_username` = NEW.username) THEN
        SIGNAL SQLSTATE '45000';
    END IF;
END;""")

connection.commit()

# cursor.execute("""
# CREATE TRIGGER PrerequisiteCheckOnAdd
# BEFORE INSERT ON Taken
# FOR EACH ROW
# BEGIN
#     IF NEW.course_id IS IN (SELECT `course_id` FROM `Has_Grade` WHERE `Has_Grade.username` = NEW.username) THEN
#         SIGNAL SQLSTATE '45000';
#     END IF;
# END;""")

# cursor.execute("""
# INSERT INTO Department(`department_id`, `name`) VALUES("CMPE", "Computer Eng");""")
# cursor.execute("""
# INSERT INTO Classroom (`classroom_id`, `campus`, `capacity`) 
# VALUES("NH101", "North", 100);""")
# connection.commit()


# cursor.execute("""
# INSERT INTO Course(`course_id`, `credits`, `name`, `quota`, `instr_username`)
# VALUES("cmpe321", 3, "databaseee", 100, "bruh");
# """)

# cursor.execute("""
# INSERT INTO Given_At(`course_id`, `classroom_id`, `time_slot`)
# VALUE("cmpe321", "NH101", 1);""")
# connection.commit()

cursor.execute("""INSERT INTO Taken(`username`, `course_id`) VALUES("bruh", "cmpe321");""")
connection.commit()


cursor.execute("""
INSERT INTO Has_Grade(`student_username`, `course_id`, `grade`) VALUES("bruh", "cmpe321", 4.0);""")

connection.commit()



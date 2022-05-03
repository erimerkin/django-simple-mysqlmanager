import mysql.connector
import environ

from pw_hasher import *

connection = mysql.connector.connect(
  host="localhost",
  user="erkin",
  password="erkin986212",
  database="SimpleBoun",
  auth_plugin="mysql_native_password"
)

cursor = connection.cursor()

# cursor.execute(
# """CREATE PROCEDURE IF NOT EXISTS `FilterCourses`(IN dept_id TEXT, IN campus TEXT, IN min_creds INT, IN max_creds INT)
# BEGIN
#     SELECT *
#     FROM Course
#     INNER JOIN Instructors ON `Instructors.username` = `Course.instr_username`
#     INNER JOIN Given_At ON `Given_At.course_id` = `Course.course_id`
#     INNER JOIN Classroom ON `Classroom.classroom_id` = `Given_At.classroom_id`
#     WHERE (`Course.credits` <= max_creds OR `Course.credits` >= min_creds) AND (`Instructors.department_id` = dept_id) AND (`Classroom.campus` = campus);
# END;""")

# cursor.execute("""
# CREATE TRIGGER ClassroomAllocation
# BEFORE INSERT ON Given_At
# FOR EACH ROW
# BEGIN
#     IF (SELECT `quota` FROM Course WHERE `course_id` = NEW.course_id) > (SELECT `capacity` FROM Classroom WHERE NEW.classroom_id = `classroom_id`) THEN 
#         DELETE FROM Course WHERE `course_id` = NEW.course_id;
#         SIGNAL SQLSTATE "45000";
#     END IF;
# END;""")

# cursor.execute("""
# CREATE TRIGGER AddCourseCheck
# BEFORE INSERT ON Taken
# FOR EACH ROW
# BEGIN
#     IF NEW.course_id IN (SELECT `course_id` FROM `Has_Grade` WHERE `student_username` = NEW.username) THEN
#         SIGNAL SQLSTATE "45000";
#     END IF;
# END;""")


# cursor.execute("""CREATE TRIGGER PrerequisiteCheckOnAdd
# BEFORE INSERT ON Taken
# FOR EACH ROW
# BEGIN
#     IF (SELECT `prereq_id` FROM `Has_Prerequisite` WHERE `Has_Prerequisite.course_id` = NEW.course_id) IN (SELECT `course_id` FROM `Has_Grade` WHERE `Has_Grade.username` = NEW.username) THEN
#         SIGNAL SQLSTATE "45000";
#     END IF;
# END;""")

# cursor.execute("""
# INSERT INTO Department(`department_id`, `name`) VALUES("CMPE", "Computer Engineering");""")
# cursor.execute("""
# INSERT INTO Department(`department_id`, `name`) VALUES("MATH", "Mathematics");""")
# cursor.execute("""
# INSERT INTO Department(`department_id`, `name`) VALUES("PHIL", "Philosophy");""")
# cursor.execute("""
# INSERT INTO Department(`department_id`, `name`) VALUES("IE", "Industrial Engineering");""")
# connection.commit()

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("faith.hancock", "{hashPassword("faithfaith11")}", "Faith", "Hancock", "hancock@simpleboun.edu.tr", "Associate Professor", "MATH"); """)

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("rosabel.eerk", "{hashPassword("eerkens1984")}", "Rosabel", "Eerkens", "eerk@simpleboun.edu.tr", "Assistant Professor", "IE") """)

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("arzucan.ozgur", "{hashPassword("mypass4321")}", "Arzucan", "Ozgur", "arzucan.ozgur@simpleboun.edu.tr", "Associate Professor", "CMPE") """)

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("simon.hunt", "{hashPassword("123abc")}", "Simon", "Hunt", "hunt.simon@simpleboun.edu.tr", "Professor", "PHIL") """)

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("sevgi.demir", "{hashPassword("dmrblk1234")}", "Sevgi", "Demirbilek", "sevgi.demir1@simpleboun.edu.tr", "Professor", "MATH") """)

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("lyuba.boer", "{hashPassword("easypass12")}", "Lyuba", "Boerio", "lyub.boerio15@simpleboun.edu.tr", "Assistant Professor", "PHIL") """)

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("park.ho", "{hashPassword("linkinpark")}", "Park", "Ho", "park.ho@simpleboun.edu.tr", "Professor", "CMPE") """)

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("nur.ulku", "{hashPassword("1nurulku1")}", "Nur", "Ulku", "ulku@simpleboun.edu.tr", "Assistant Professor", "CMPE") """)

# cursor.execute(f"""
# INSERT INTO Instructors(`username`, `password`, `name`, `surname`, `email`, `title`,`department_id`)
# VALUES("charles.sutherland", "{hashPassword("princecharles")}", "Charles", "Sutherland", "sutherland@simpleboun.edu.tr", "Professor", "CMPE") """)


cursor.execute(f"""
INSERT INTO Students(`username`, `password`, `name`, `surname`, `email`, `student_id`, `department_id`, `GPA`, `credits`)
VALUES ("berke.argin", "{hashPassword("newyork123")}", "Berke", "Argin", "berke.argin@simpleboun.edu.tr", 16080, "MATH", 0, 0);""")
# cursor.execute(f"""
# INSERT INTO Students(`username`, `password`, `name`, `surname`, `email`, `student_id`, `department_id`, `GPA`, `credits`)
# VALUES ("niyazi.ulke", "{hashPassword("mypass")}", "Niyazi", "Ulke", "ulke@simpleboun.edu.tr", 17402, "CMPE", 0, 0);""")
# cursor.execute(f"""
# INSERT INTO Students(`username`, `password`, `name`, `surname`, `email`, `student_id`, `department_id`, `GPA`, `credits`)
# VALUES ("ryan.andrews", "{hashPassword("pass4321")}", "Ryan", "Andrews", "andrews@simpleboun.edu.tr", 18321, "PHIL", 0, 0);""")
# cursor.execute(f"""
# INSERT INTO Students(`username`, `password`, `name`, `surname`, `email`, `student_id`, `department_id`, `GPA`, `credits`)
# VALUES ("he.gongmin", "{hashPassword("passwordpass")}", "He", "Gongmin", "he.gongmin@simpleboun.edu.tr", 19333, "IE", 0, 0);""")
# cursor.execute(f"""
# INSERT INTO Students(`username`, `password`, `name`, `surname`, `email`, `student_id`, `department_id`, `GPA`, `credits`)
# VALUES ("carm.galian", "{hashPassword("madrid9897")}", "Carmelita", "Galiano", "carm.galian@simpleboun.edu.tr", 19356, "PHIL", 0, 0);""")
# cursor.execute(f"""
# INSERT INTO Students(`username`, `password`, `name`, `surname`, `email`, `student_id`, `department_id`, `GPA`, `credits`)
# VALUES ("kron.helene", "{hashPassword("helenepass")}", "Helene", "Kron", "kron.helene@boun.edu.tr", 20341, "CMPE", 0, 0);""")

# cursor.execute("""
# INSERT INTO Classroom(`classroom_id`, `campus`, `capacity`) VALUES("HD201", "Hisar Campus", 300);)""")

# cursor.execute("""
# INSERT INTO Classroom(`classroom_id`, `campus`, `capacity`) VALUES("BMA2", "North Campus", 200);)""")

# cursor.execute("""
# INSERT INTO Classroom(`classroom_id`, `campus`, `capacity`) VALUES("BMA3", "North Campus", 150);)""")

# cursor.execute("""
# INSERT INTO Classroom(`classroom_id`, `campus`, `capacity`) VALUES("TB310", "South Campus", 100);)""")

# cursor.execute("""
# INSERT INTO Classroom(`classroom_id`, `campus`, `capacity`) VALUES("M1171", "South Campus", 100);)""")

# cursor.execute(f"""
# INSERT INTO DBManager(`username`, `password`) VALUES("manager1", "{hashPassword('managerpass1')}");""")
# cursor.execute(f"""
# INSERT INTO DBManager(`username`, `password`) VALUES("manager2", "{hashPassword('managerpass2')}");""")
# cursor.execute(f"""
# INSERT INTO DBManager(`username`, `password`) VALUES("manager35", "{hashPassword('managerpass35')}");""")

connection.commit()



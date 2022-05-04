import mysql.connector
import environ
from utilities import encrypt_password

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

# cursor.execute(f"""INSERT INTO `Classroom` (`classroom_id`, `campus`, `capacity`)
# VALUES ('BMA2', 'North Campus', 200),
#     ('BMA3', 'North Campus', 150),
#     ('HD201', 'Hisar Campus', 300),
#     ('M1171', 'South Campus', 100),
#     ('TB310', 'South Campus', 100);""")

# cursor.execute(f"""INSERT INTO `Department` (`department_id`, `name`)
# VALUES ('CMPE', 'Computer Engineering'),
#     ('IE', 'Industrial Engineering'),
#     ('MATH', 'Mathematics'),
#     ('PHIL', 'Philosophy');""")

# connection.commit()

cursor.execute(f"""INSERT INTO `Students` (`username`, `name`, `surname`, `email`, `password`, `department_id`, `student_id`)
VALUES
    ('berke.argin', 'Berke', 'Argin', 'berke.argin@simpleboun.edu.tr', "{encrypt_password("newyork123")}", 'MATH', 16080),
	('carm.galian','Carmelita','Galiano','carm.galian@simpleboun.edu.tr',"{encrypt_password("madrid9897")}",'PHIL',19356),
	('erkin','erkin','dogan','erkin@gmail.com',"{encrypt_password("erkin")}",'CMPE',2019400225),
	('he.gongmin','He','Gongmin','he.gongmin@simpleboun.edu.tr',"{encrypt_password("passwordpass")}",'IE',19333),
	('kron.helene','Helene','Kron','kron.helene@boun.edu.tr',"{encrypt_password("helenepass")}",'CMPE',20341),
	('niyazi.ulke','Niyazi','Ulke','ulke@simpleboun.edu.tr',"{encrypt_password("mypass")}",'CMPE',17402),
	('ryan.andrews','Ryan','Andrews','andrews@simpleboun.edu.tr',"{encrypt_password("pass4321")}",'PHIL',18321);""")

cursor.execute(f"""INSERT INTO `Instructors` (`username`, `name`, `surname`, `email`, `password`, `department_id`, `title`)
VALUES
	('arzucan.ozgur','Arzucan','Ozgur','arzucan.ozgur@simpleboun.edu.tr','{encrypt_password("mypass4321")}','CMPE','Associate Professor'),
	('charles.sutherland','Charles','Sutherland','sutherland@simpleboun.edu.tr','{encrypt_password("princecharles")}','CMPE','Professor'),
	('erkin','temp','temp','temp','{encrypt_password("erkin")}','MATH','Professor'),
	('faith.hancock','Faith','Hancock','hancock@simpleboun.edu.tr','{encrypt_password("faithfaith11")}','MATH','Associate Professor'),
	('lyuba.boer','Lyuba','Boerio','lyub.boerio15@simpleboun.edu.tr','{encrypt_password("easypass12")}','PHIL','Assistant Professor'),
	('nur.ulku','Nur','Ulku','ulku@simpleboun.edu.tr','{encrypt_password("1nurulku1")}','CMPE','Assistant Professor'),
	('park.ho','Park','Ho','park.ho@simpleboun.edu.tr','{encrypt_password("linkinpark")}','CMPE','Professor'),
	('rosabel.eerk','Rosabel','Eerkens','eerk@simpleboun.edu.tr','{encrypt_password("eerkens1984")}','IE','Assistant Professor'),
	('sevgi.demir','Sevgi','Demirbilek','sevgi.demir1@simpleboun.edu.tr','{encrypt_password("dmrblk1234")}','MATH','Professor'),
	('simon.hunt','Simon','Hunt','hunt.simon@simpleboun.edu.tr','{encrypt_password("123abc")}','PHIL','Professor');""")

# cursor.execute(f"""INSERT INTO `DBManager` (`username`, `password`)
# VALUES
# 	('manager1','{encrypt_password("managerpass1")}'),
# 	('manager2','{encrypt_password("managerpass2")}'),
# 	('manager35','{encrypt_password("managerpass35")}'),
# 	('erkin','{encrypt_password("erkin")}'),
# 	('omer','{encrypt_password("omer")}');""")

connection.commit()
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    usuario = "usuario",
    senha = "senha",
    dataBase = "banco_de_dados"
)



cursor = db.cursor()

sql = "INSERT INFO sensores(temp,pressao) VALUES(%s,%s)"
val = [("s0.5","1010.1")
("20.1", "1008.8"),
("20.3", "1009.7"),
("20.5", "1010.6"),
("20.2", "1011.5"), 
("20.4", "1010.4"), 
("20.1", "1011.1"), 
("20.3", "1010.0")]
cursor.execute(sql,val)
db.comit()
print(cursor.rowcount,"registros inseridos com sucesso.")

cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)
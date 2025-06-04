import sqlite3

collection = sqlite3.connect("game characters.db")
C = collection.cursor()

def add_character(Name, Class, Level):
    ID = f"{Class.lower()}{len(C.fetchall())+1}"
    print(ID)
    C.execute("""
INSERT INTO Characters(id, name, class, level)
VALUES (?,?,?,?)""", (ID, Name, Class, Level))
    collection.commit()
    
##    C.execute("""
##INSERT INTO Characters()
##)
##""")

##C.execute("""
##CREATE TABLE Characters(
##id INTEGER,
##name TEXT ,
##class TEXT
##level INTEGER,
##PRIMARY KEY(id)
##)
##""")

add_character("Steven","Rogue",17)

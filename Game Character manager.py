import sqlite3
from validation_scripts import *

collection = sqlite3.connect("game characters.db")
C = collection.cursor()

# Creating the Table
def create_table():
    C.execute("""
CREATE TABLE IF NOT EXISTS Characters(
id TEXT NOT NULL,
name TEXT NOT NULL,
class TEXT NOT NULL,
level INTEGER NOT NULL,
PRIMARY KEY(id)
)
""")
    collection.commit()

# Adding character to the table
def add_character(Name, Class, Level):

# Select Clause
    C.execute(f"""
SELECT * FROM Characters
              WHERE class = '{Class}'
              """)
    characters = C.fetchall()

# If the table is empty
    if len(characters) == 0:
        ID = Class + "1"
    else:
        serial_numb = 1
        exists = True

#Nested loop to check for alrady existing IDs and choose the smallest one
        while exists:
            for entry in characters:
                if entry[0] == f"{Class}{serial_numb}":
                    exists = True
                    serial_numb += 1
                    break
                else:
                    exists = False
        ID = f"{Class}{serial_numb}"

# Insert clause
    C.execute("""
INSERT INTO Characters(id, name, class, level)
VALUES (?,?,?,?)""", (ID, Name, Class, Level))
    collection.commit()

def view_table():
    C.execute("""
SELECT * FROM Characters""")
    data = C.fetchall()
    headers = ["ID","Name","Class","Level"]
    table = ""
    if data == []:
        table = "|         No entries        |\n"
    else:
        # Records
        for line in data:
            formatted = "| "
            # Each record's attributes
            for attribute in line:
                #Empty space here to make the size of the box consistent fro the header and records
                if attribute == line[0]:
                    headers[0] = headers[0] + " "*max(len(attribute)-len(headers[0]), 0)
                    formatted += attribute + " "*max(len(headers[0])-len(attribute), 0) + " | "

                elif attribute == line[1]:
                    headers[1] = headers[1] + " "*max(len(attribute)-len(headers[1]), 0)
                    formatted += attribute + " "*max(len(headers[1])-len(attribute), 0) + " | "

                elif attribute == line[2]:
                    headers[2] = headers[2] + " "*max(len(attribute)-len(headers[2]), 0)
                    formatted += attribute + " "*max(len(headers[2])-len(attribute), 0) + " | "

                elif attribute == line[3]:
                    attribute = str(attribute)
                    headers[3] = headers[3] + " "*max(len(attribute)-len(headers[3]), 0)
                    formatted += attribute + " "*max(len(headers[3])-len(attribute), 0) + " |\n"

            table += formatted

    #separate line for the top and bottom border, the header names and the separator
    top_line = "◸" + "—"*(11+sum(len(headers[a]) for a in range(len(headers)))) + "◹" + "\n"
    columns = f"| {headers[0]} | {headers[1]} | {headers[2]} | {headers[3]} |" + "\n"
    middle_line = "|" + "—"*(11+sum(len(headers[a]) for a in range(len(headers)))) + "|" + "\n"
    bottom_line = "◺" + "—"*(11+sum(len(headers[a]) for a in range(len(headers)))) + "◿"
    table = top_line + columns + middle_line + table + bottom_line
    print("◈Character Database◈")
    print(table)

def update_character(Target_ID, NewName="", NewClass="", NewLevel=None):
    #Checking if target is in the database
    C.execute(f"""
SELECT * FROM Characters
              WHERE id = '{Target_ID}'
              """)
    target_character = C.fetchone()

    #Keeping original data if not passing in function
    if NewName == "":
        NewName = target_character[1]
    if NewClass == "":
        NewClass = target_character[2]
    if NewLevel == "":
        NewLevel = target_character[3]

        #Select Clause
    C.execute(f"""
SELECT * FROM Characters
            WHERE class = '{NewClass}'
            """)
    characters = C.fetchall()

# If the table is empty
    if len(characters) == 0:
        ID = NewClass + "1"
    else:
        serial_numb = 1
        exists = True

#Nested loop to check for alrady existing IDs and choose the smallest one
        while exists:
            for entry in characters:
                if entry[0] == f"{NewClass}{serial_numb}":
                    exists = True
                    serial_numb += 1
                    break
                else:
                    exists = False
        ID = f"{NewClass}{serial_numb}"

        
    C.execute(f"""
UPDATE Characters
SET id = '{ID}',name = '{NewName}', class = '{NewClass}', level = '{NewLevel}'
WHERE id = '{Target_ID}'
            """)
    collection.commit()
    return True

def delete_character(Target_ID):
    #Checking if target is in the database
    C.execute(f"""
SELECT * FROM Characters
              WHERE id = '{Target_ID}'
              """)
    target_character = C.fetchone()
    if target_character is None:
        print("Not in database!")

    else:
    #Deleting target from database
        C.execute(f"""
DELETE FROM Characters
WHERE id = '{Target_ID}'
""")

running = True
create_table()
print("Welcome to the Game Character Manager!\n")
while running:
    choice = ""
    while choice not in ["1","2","3","4","5"]:
        choice = input("""What would you like to do?
1. Add Character
2. View All Characters
3. Update Character
4. Delete Character
5. Exit
                       
Enter your choice:
""")
        if choice not in ["1","2","3","4","5"]:
            print(f"\nI'm sorry, I don't know what '{choice}' means.")
        else:
            print("")

    if choice == "1":
        print("Add Character\n")
        character_info = {"Name":"",
                          "Class":"",
                          "Level":0}
        
        valid = False
        while not valid:
            choice = input("Please enter the character's name\n")
            if not validate_name(choice):
                print("\nI'm sorry, but this isn't a proper name.")
            elif choice == "":
                print("\nI need a name, please.")                
            else:
                valid = True
                character_info["Name"] = choice
                

        valid = False
        print("")
        while not valid:
            choice = input("Please enter the character's class\n")
            if not validate_class(choice):
                print("\nI'm sorry, but this isn't a proper class name.")
            elif choice == "":
                print("\nI need a class name, please.")                
            else:
                valid = True
                character_info["Class"] = choice

        valid = False
        print("")
        while not valid:
            choice = input("Please enter the character's level\n")
            if not validate_int(choice):
                print("Unfortunately, you can only have numeric level values.")
            elif choice == "":
                choice = 0
            else:
                valid = True
                character_info["Level"] = choice

        add_character(character_info["Name"],character_info["Class"],character_info["Level"])

        print(f"\n{character_info["Name"]} has been added to the character table!\n")
                

    if choice == "2":
        view_table()

    if choice == "3":
        valid = False
        print("Here's the table to find the character you want to update\n")
        view_table()
        print("")
        while not valid:
            choice = input("Please enter ID\n")
            C.execute(f"""
            SELECT * FROM Characters
                        WHERE id = '{choice}'
                        """)
            target_character = C.fetchone()
            if target_character == []:
                print(f"ID '{choice}' is either misspelt or non-existent\n")
            else:
                valid = True
                current_ID = choice

        new_character_info = {"Name":"",
                          "Class":"",
                          "Level":0}
        
        valid = False
        while not valid:
            choice = input("Please enter the character's new name\n")
            if not validate_name(choice):
                print("\nI'm sorry, but this isn't a proper name.")
            elif choice == "":
                print("\nI need a name, please.")   
            else:
                valid = True
                new_character_info["Name"] = choice
                

        valid = False
        print("")
        while not valid:
            choice = input("Please enter the character's new class\n")
            if not validate_class(choice):
                print("\nI'm sorry, but this isn't a proper class name.")
            elif choice == "":
                print("\nI need a class name, please.")
            else:
                valid = True
                new_character_info["Class"] = choice

        valid = False
        print("")
        while not valid:
            choice = input("Please enter the character's new level\n")
            if not validate_int(choice):
                print("Unfortunately, you can only have numeric level values.")
            elif choice == "":
                choice = "0"
            else:
                valid = True
                new_character_info["Level"] = choice

        choice = ""
        while choice.upper() not in ["Y","N"]:
            choice = input("\nAre you sure you want to commit to these changes? - Y/N\n")
            if choice.upper() not in ["Y","N"]:
                print("\nPlease confirm in the format: Y/N")
            elif choice.upper() == "Y":
                update_character(current_ID, new_character_info["Name"], new_character_info["Class"], new_character_info["Level"])
                print(f"\n{target_character[1]} has been updated to {new_character_info["Name"]} in class {new_character_info["Class"]} and level {new_character_info["Level"]}\n")
            else:
                print("\nDiscarding changes\n") 


    if choice == "4":
        valid = False
        print("Here's the table to find the character you want to delete\n")
        view_table()
        print("")
        while not valid:
            choice = input("Please enter ID\n")
            C.execute(f"""
            SELECT * FROM Characters
                        WHERE id = '{choice}'
                        """)
            target_character = C.fetchone()
            if target_character == []:
                print(f"ID '{choice}' is either misspelt or non-existent\n")
            else:
                valid = True
                current_ID = choice

        choice = ""
        while choice.upper() not in ["Y","N"]:
            choice = input("\nAre you sure you want to commit to these changes? - Y/N\n")
            if choice.upper() not in ["Y","N"]:
                print("\nPlease confirm in the format: Y/N")
            elif choice.upper() == "Y":
                delete_character(current_ID)
                print(f"\n{target_character[1]} has been deleted")
            else:
                print("\nDiscarding changes\n")

    if choice == "5":
        while choice.upper() not in ["Y","N"]:
            choice = input("\nAre you sure you want to exit? - Y/N\n")
            if choice.upper() not in ["Y","N"]:
                print("\nPlease confirm in the format: Y/N")
            elif choice.upper() == "Y":
                print(f"Exiting...")
                running = False
            else:
                print("\nReturning to beginning...\n")
C.close()
#CRUD=CREATE<READ<UPDATE<DELETE
import sqlite3
import csv
def create_connection():
    try:
        con=sqlite3.connect('users.sqlite3')
        return con
    except Exception as e:
        print(e)

INPUT_STRING="""
Enter the option: FROM CSV INTO USERS TABLE
    1.CREATE TABLE
    2.DUMP USERS FROM CSV INTO USERS TABLE
    3.ADD NEW  USER INTO USERS TABLE
    4.QUERY ALL USERS FROM TABLE
    5.QUERY USER BY ID FROM TABLE
    6.QUERY SPECIFIED NO. OF RECORDS FROM TABLE
    7.DELETE ALL USERS
    8.DELETE USER BY ID
    9.UPDATE USER
    10.PRESS ANY KEY TO EXIT
"""
def create_table(con):
    CREATE_USERS_TABLE_QUERY="""
         CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              first_name CHAR(255) NOT NULL,
              last_name CHAR(255) NOT NULL,
              company_name CHAR(255) NOT NULL,
              address CHAR(255) NOT NULL,
              city CHAR(255) NOT NULL,
              county CHAR(255) NOT NULL,
              state CHAR(255) NOT NULL,
              zip REAL NOT NULL,
              phone1 CHAR(255) NOT NULL,
              phone2 CHAR(255) NOT NULL,
              email CHAR(255) NOT NULL,
              web text
              
            );
          """
    cur=con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print ('User table was creates succcessfully.')



 
def read_csv():
    users=[]
    with open("sample_users.csv") as f:
        data=csv.reader(f)
        for user in data:
            users.append(tuple(user))
    return users[1:]



def insert_users(con,users):
    user_add_query="""
    INSERT INTO users
    (
      first_name,
      last_name,
      company_name,
      address,
      city,
      county,
      state,
      zip,
      phone1,
      phone2,
      email,
      web
      )
      values(?,?,?,?,?,?,?,?,?,?,?,?);
    """
    cur=con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f"{len(users)}users were imported succesfully")

COLUMNS=(
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web"
)

def select_users(con,no_of_users=0):
    cur=con.cursor()
    if no_of_users:
       users=cur.execute("SELECT * FROM users LIMIT ?;",(no_of_users,))
    else:
        users=cur.execute("SELECT * FROM users;")      
    
    for user in users:
        print(user) 

def select_user_by_id(con,user_id):
    cur=con.cursor()
    users=cur.execute("SELECT * FROM users WHERE id=?;",(user_id,))
    for user in  users:
        print(user)   
def delete_user(con):
    cur=con.cursor()
    cur.execute("DELETE from users;")
    con.commit()
    print("ALL users were deleted successfully.")
def delete_user_by_id(con,user_id):
    cur=con.cursor()
    delete_id=cur.execute("DELETE from users where id=?;",(user_id,))
    con.commit()
    print('USER DELETED')
def update_user_by_id(con,user_id,column_name,column_value):
    update_query=input(f"UPDATE users set {column_name}=? where id=?;")
    cur=con.cursor()
    cur.execute(update_query,(column_value,user_id))
    con.commit()
    print(f"[{column_name} was updated with value [{column_value}] of user with id [{user_id}]")

def main():
    con=create_connection()
    if con:
        user_input=input(INPUT_STRING)
        if user_input=='1':
            create_table(con)    
        elif user_input=='2':
            users=read_csv()
            print(users)
            insert_users(con,users)
        elif user_input=='3':
            user_data=[]
            for column in COLUMNS:
                column_value=input(f"ENTER ther value of {column}:")
                user_data.append(column_value)  
            insert_users(con,[tuple(user_data)])    

        elif user_input=='4':
            select_users(con)
        elif user_input=='5':
            user_id=input('enter ur id:')
            select_user_by_id(con,user_id)
        elif user_input=='6':
            no_of_users=input("ENTER NO. OF RECORDS:")
            select_users(con,no_of_users)
        elif user_input=='7':
            confirmation=input("ARE YOU SURE YOU WANT TO DELETE Y OR N?:")
            if confirmation=='Y':
                delete_user(con)
        elif user_input=='8':
            user_id=input("ENTER USER ID TO DELETE:")
            delete_user_by_id(con,user_id)
        elif user_input=='9':
             user_id=input('ENTER ID OF USER:')
             if user_id.isnumeric():
                column_name=input(f"ENTER THE COLUMN YOU WANT TO EDIT.PLEASE MAKE SURE COLUMN IS WITHIN{COLUMNS}:")
                if column_name in COLUMNS:
                    column_value=input(f"ENTER THE VALUE OF {column_name}:")
                    update_user_by_id(con,user_id,column_name,column_value)
                
        elif user_input=='10':
            exit()

main()      
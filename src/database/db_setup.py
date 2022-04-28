import os
import sqlite3

exit(
    "ALL YOUR DATA WILL BE LOST !!!!\nComment this line if you want to reset "
    "your database.\nALL YOUR DATA WILL BE LOST !!!!"
)

database_path = "../data/test.db"

os.remove(database_path)
print("Database deleted")

con = sqlite3.connect(database_path)
print("Database created")
cur = con.cursor()

cur.execute(
    """
            create table user_data (id integer primary key, school_id 
            string, class_id string, alerts_enabled boolean, 
            alert_time integer)
            """
)

cur.execute(
    """
            create table guild_data 
            (id integer primary key, school_id string, class_id string, 
            schedule_channel_id integer, alerts_enabled boolean, 
            alert_time integer, alert_role_id integer)
            """
)

print("Created database tables")

con.commit()
con.close()

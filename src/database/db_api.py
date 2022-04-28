import collections
import sqlite3

database_path = "../data/test.db"

""" USER DATA """


def get_user_data(user_id: int):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute("select * from user_data where id=:userid", {"userid": user_id})

    fetch = cur.fetchall()
    if not fetch:
        return None
    data_tuple = fetch[0]
    _id = data_tuple[0]
    school_id = data_tuple[1]
    class_id = data_tuple[2]
    alerts_enabled = bool(data_tuple[3])
    alert_time = data_tuple[4]

    UserData = collections.namedtuple(
        "UserData", ["id", "school_id", "class_id", "alerts_enabled", "alert_time"]
    )

    con.close()

    return UserData(_id, school_id, class_id, alerts_enabled, alert_time)


def set_user_data(
    user_id, *, school_id=None, class_id=None, alerts_enabled=None, alert_time=None
):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    if not user_exists_in_database(user_id):
        cur.execute(
            """
            insert or replace into user_data(id) values (:user_id)
            """,
            {"user_id": user_id},
        )

    if school_id is not None:
        cur.execute(
            """
            update user_data set school_id =:school_id 
            WHERE id=:user_id""",
            {"school_id": school_id, "user_id": user_id},
        )
    if class_id is not None:
        cur.execute(
            """
            update user_data set class_id =:class_id 
            WHERE id=:user_id""",
            {"class_id": class_id, "user_id": user_id},
        )
    if alerts_enabled is not None:
        cur.execute(
            """
            update user_data set alerts_enabled =:alerts_enabled 
            WHERE id=:user_id""",
            {"alerts_enabled": alerts_enabled, "user_id": user_id},
        )
    if alert_time is not None:
        cur.execute(
            """
            update user_data set alert_time =:alert_time 
            WHERE id=:user_id""",
            {"alert_time": alert_time, "user_id": user_id},
        )

    con.commit()
    con.close()


def reset_user_data(user_id):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(
        """
        delete from user_data WHERE id=:user_id""",
        {"user_id": user_id},
    )
    con.commit()
    con.close()


def user_exists_in_database(user_id):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute("""select id from user_data where id=:user_id""",
                {"user_id": user_id})
    fetch = cur.fetchone()
    con.close()

    if fetch is None:
        return False
    return True


""" GUILD DATA """


def get_guild_data(guild_id: int):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(
        """
                select * from guild_data where id=:guild_id""",
        {"guild_id": guild_id},
    )
    fetch = cur.fetchall()
    if not fetch:
        return None
    data_tuple = fetch[0]
    _id = data_tuple[0]
    school_id = data_tuple[1]
    class_id = data_tuple[2]
    schedule_channel_id = data_tuple[3]
    alerts_enabled = bool(data_tuple[4])
    alert_time = data_tuple[5]
    alert_role_id = data_tuple[6]

    GuildData = collections.namedtuple(
        "GuildData",
        [
            "id",
            "school_id",
            "class_id",
            "schedule_channel_id",
            "alerts_enabled",
            "alert_time",
            "alert_role_id",
        ],
    )

    con.close()

    return GuildData(
        _id,
        school_id,
        class_id,
        schedule_channel_id,
        alerts_enabled,
        alert_time,
        alert_role_id,
    )


def set_guild_data(
    guild_id,
    *,
    school_id=None,
    class_id=None,
    schedule_channel_id=None,
    alerts_enabled=None,
    alert_time=None,
    alert_role_id=None
):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    if not user_exists_in_database(guild_id):
        cur.execute(
            """
            insert or replace into guild_data(id) values (:guild_id)
            """,
            {"guild_id": guild_id},
        )

    if school_id is not None:
        cur.execute(
            """
            update guild_data set school_id =:school_id 
            WHERE id=:guild_id""",
            {"school_id": school_id, "guild_id": guild_id},
        )
    if class_id is not None:
        cur.execute(
            """
            update guild_data set class_id =:class_id 
            WHERE id=:guild_id""",
            {"class_id": class_id, "guild_id": guild_id},
        )
    if schedule_channel_id is not None:
        cur.execute(
            """
            update guild_data set schedule_channel_id =:schedule_channel_id 
            WHERE id=:guild_id""",
            {"schedule_channel_id": schedule_channel_id, "guild_id": guild_id},
        )

    if alerts_enabled is not None:
        cur.execute(
            """
            update guild_data set class_id =:class_id 
            WHERE id= :guild_id;""",
            {"class_id": class_id, "guild_id": guild_id},
        )
        if alert_time is not None:
            cur.execute(
                """
                update guild_data set alert_time =:alert_time 
                WHERE id=:guild_id""",
                {"alert_time": alert_time, "guild_id": guild_id},
            )
        if alert_role_id is not None:
            cur.execute(
                """
                update guild_data set alert_role_id =:alert_role_id 
                WHERE id=:guild_id""",
                {"alert_role_id": alert_role_id, "guild_id": guild_id},
            )

    con.commit()
    con.close()


def guild_exists_in_database(guild_id):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(
        """select id from guild_data where id=:guild_id""", {"guild_id": guild_id}
    )
    fetch = cur.fetchone()
    con.close()

    if fetch is None:
        return False
    return True

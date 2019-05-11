import sqlite3


def start():
    global connection, crsr
    connection = sqlite3.connect("servers.db")
    crsr = connection.cursor()

def create_servers_table():
    global connection, crsr
    sql_command = """CREATE TABLE IF NOT EXISTS servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id VARCHAR(20),
    chat_channel VARCHAR(20),
    ascii_art INT,
    server_name VARCHAR(50));"""
    crsr.execute(sql_command)

def ifRecord(server_id):
    global connection, crsr
    sql_command = "SELECT COUNT(1)\n    FROM servers\n    WHERE server_id = \"%s\";"%server_id
    crsr.execute(sql_command)
    if crsr.fetchall()[0][0] == 0:
        return False
    else:
        return True

def close():
    global connection, crsr
    connection.commit()
    connection.close()

def update_channel(server, val):
    global connection, crsr

    if not ifRecord(server.id):
        sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", 1, \"%s\");" %(server.id, server.name)
        crsr.execute(sql_command)
        print("added server: %s"%server)

    sql_command = "UPDATE servers SET chat_channel = \"%s\" WHERE server_id = \"%s\"" %(val, server.id) # dont work
    crsr.execute(sql_command)

def update_ascii(server, val):
    global connection, crsr

    if not ifRecord(server.id):
        sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", 1, \"%s\");" %(server.id, server.name)
        crsr.execute(sql_command)
        print("added server: %s"%server)

    sql_command = "UPDATE servers SET ascii_art = %s WHERE server_id = \"%s\"" %(val, server.id) # dont work
    crsr.execute(sql_command)


def is_ascii(server):
    global connection, crsr

    if not ifRecord(server.id):
        sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", 1, \"%s\");" %(server.id, server.name)
        crsr.execute(sql_command)
        print("added server: %s"%server)

    sql_command = "SELECT ascii_art FROM servers WHERE server_id = \"%s\";"%server.id
    crsr.execute(sql_command)
    return crsr.fetchall()[0][0]

def get_chat(server):
    global connection, crsr
    if not ifRecord(server.id):
        sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", 1, \"%s\");" %(server.id, server.name)
        crsr.execute(sql_command)
        print("added server: %s"%server)

    sql_command = "SELECT chat_channel FROM servers WHERE server_id = \"%s\";"%server
    crsr.execute(sql_command)
    out = crsr.fetchall()[0][0]
    if out == "0":
        return False
    return out

def all_chat():
    global connection, crsr
    sql_command = "SELECT chat_channel FROM servers;"
    crsr.execute(sql_command)
    out = list()
    for i in crsr.fetchall():
        if not i[0] == "0":
            out.append(i[0])
    return out



if __name__ == '__main__':
    start()

    create_servers_table() # makes the empty database

    close()

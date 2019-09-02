import sqlite3


class database(sqlite3.Connection):
    def __init__(self, db):
        self.db = db

        self.create_servers_table()

    def create_servers_table(self):
        sql_command = """CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_id VARCHAR(20),
        chat_channel VARCHAR(20),
        ticket_cat VARCHAR(20),
        botprefix VARCHAR(1),
        ascii_art INT,
        server_name VARCHAR(50));"""
        self.db.execute(sql_command)

    def ifRecord(self, server_id):
        sql_command = "SELECT COUNT(1)\n    FROM servers\n    WHERE server_id = \"%s\";"%server_id
        self.db.execute(sql_command)
        if self.db.fetchall()[0][0] == 0:
            return False
        else:
            return True


    def update_channel(self, server, val):
        if not self.ifRecord(server.id):
            sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", NULL, NULL, 1, \"%s\");" %(server.id, server.name)
            self.db.execute(sql_command)
            print("added server: %s"%server)

        sql_command = "UPDATE servers SET chat_channel = \"%s\" WHERE server_id = \"%s\"" %(val, server.id) # dont work
        self.db.execute(sql_command)

    def update_ticket_cat(server, val):
        if not self.ifRecord(server.id):
            sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", NULL, NULL, 1, \"%s\");" %(server.id, server.name)
            self.db.execute(sql_command)
            print("added server: %s"%server)

        sql_command = "UPDATE servers SET ticket_cat = \"%s\" WHERE server_id = \"%s\"" %(val, server.id) # dont work
        self.db.execute(sql_command)

    def update_ascii(server, val):
        if not self.ifRecord(server.id):
            sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", NULL, NULL, 1, \"%s\");" %(server.id, server.name)
            self.db.execute(sql_command)
            print("added server: %s"%server)

        sql_command = "UPDATE servers SET ascii_art = %s WHERE server_id = \"%s\"" %(val, server.id) # dont work
        self.db.execute(sql_command)

    def update_prefix(server, val):
        if not self.ifRecord(server.id):
            sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", NULL, NULL, 1, \"%s\");" %(server.id, server.name)
            self.db.execute(sql_command)
            print("added server: %s"%server)

        sql_command = "UPDATE servers SET botprefix = \"%s\" WHERE server_id = \"%s\"" %(val, server.id) # dont work
        self.db.execute(sql_command)


    def is_ascii(server):
        if not self.ifRecord(server.id):
            sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", NULL, NULL, 1, \"%s\");" %(server.id, server.name)
            self.db.execute(sql_command)
            print("added server: %s"%server)

        sql_command = "SELECT ascii_art FROM servers WHERE server_id = \"%s\";"%server.id
        self.db.execute(sql_command)
        return self.db.fetchall()[0][0]

    def get_chat(server):
        if not self.ifRecord(server.id):
            sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", NULL, NULL, 1, \"%s\");" %(server.id, server.name)
            self.db.execute(sql_command)
            print("added server: %s"%server)

        sql_command = "SELECT chat_channel FROM servers WHERE server_id = \"%s\";"%server
        self.db.execute(sql_command)
        out = self.db.fetchall()[0][0]
        if out == "0":
            return False
        return out

    def get_ticket(server):
        if not self.ifRecord(server.id):
            sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", NULL, NULL, 1, \"%s\");" %(server.id, server.name)
            self.db.execute(sql_command)
            print("added server: %s"%server)

        sql_command = "SELECT ticket_cat FROM servers WHERE server_id = \"%s\";"%server.id
        self.db.execute(sql_command)
        out = self.db.fetchall()[0][0]
        if out == "0":
            return False
        return out

    def get_prefix(server):
        if not self.ifRecord(server.id):
            sql_command = "INSERT INTO servers VALUES (NULL, \"%s\", \"0\", NULL, NULL, 1, \"%s\");" %(server.id, server.name)
            self.db.execute(sql_command)
            print("added server: %s"%server)

        sql_command = "SELECT botprefix FROM servers WHERE server_id = \"%s\";"%server
        self.db.execute(sql_command)
        out = self.db.fetchall()[0][0]
        if out == "0":
            return "?"
        return out

    def all_chat(self):
        sql_command = "SELECT chat_channel FROM servers;"
        self.db.execute(sql_command)
        out = list()
        for i in self.db.fetchall():
            if not i[0] == "0":
                out.append(i[0])
        return out

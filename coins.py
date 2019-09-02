import sqlite3


class database(sqlite3.Connection):
    def __init__(self, db):
        self.db = db

        self.create_money_table()


    def create_money_table(self):
        global connection, crsr
        sql_command = """
        CREATE TABLE IF NOT EXISTS balances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id VARCHAR(20),
        amount DESCIMAL);"""
        self.db.execute(sql_command)

    def ifRecord(self, user_id):
        global connection, crsr
        sql_command = "SELECT COUNT(1)\n    FROM balances\n    WHERE user_id = \"%s\";"%user_id
        self.db.execute(sql_command)
        if self.db.fetchall()[0][0] == 0:
            return False
        else:
            return True


    def balance(self, user_id):
        if self.ifRecord(user_id):
            sql_command = "SELECT amount FROM balances WHERE user_id = %s" %user_id
            self.db.execute(sql_command)
            return self.db.fetchall()[0][0]
        else:
            sql_command = "INSERT INTO balances VALUES (NULL, %s, 0)" %user_id
            self.db.execute(sql_command)
            print("Added %s to coins db" %user_id)
            return 0

    def add(self, user_id, amt):
        sql_command = "UPDATE balances SET amount = %s WHERE user_id = %s" %(self.balance(user_id)+amt, user_id)
        self.db.execute(sql_command)
        return True

    def buy(self, user_id, amt):
        return self.create(user_id, amt)

    def create(self, user_id, amt):
        return self.add(user_id, amt)

    def send(self, from_user, to_user, amt):
        if amt > 0:
            if (self.balance(from_user) - amt) >= 0:
                self.add(from_user, -amt)
                self.add(to_user, amt)
                return (True, "Successfull")
            else:
                return (False, "Insufficient funds")
        else:
            return (False, "Can not send negative amount")

    def top(self, users):
        sql_command = "SELECT * FROM balances ORDER BY amount DESC LIMIT %s;"%users
        self.db.execute(sql_command)
        return self.db.fetchall()

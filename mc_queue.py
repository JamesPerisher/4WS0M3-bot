import urllib.request as request
import json
import sqlite3
import time
import matplotlib.pyplot as plt

que_update = 10*60

#===========================DATABASE===========================

def start():
    global connection, crsr
    connection = sqlite3.connect("data/queue.db")
    crsr = connection.cursor()

def create_queue_all_table():
    global connection, crsr
    sql_command = """CREATE TABLE IF NOT EXISTS que_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    queue INTEGER,
    online INTEGER,
    time INTEGER);"""
    crsr.execute(sql_command)

def add(que, online):
    global connection, crsr
    sql_command = "INSERT INTO que_history VALUES (NULL, \"%s\", \"%s\", \"%s\");" %(que, online, str(time.time()).split(".")[0])
    crsr.execute(sql_command)

def get24():
    global connection, crsr
    sql_command = "SELECT * FROM que_history ORDER BY id desc LIMIT %s;" %(24*60*60/que_update)
    crsr.execute(sql_command)

    return crsr.fetchall()

def get_last():
    global connection, crsr
    sql_command = "SELECT * FROM que_history ORDER BY id desc LIMIT 1;"
    crsr.execute(sql_command)

    return crsr.fetchall()


def close():
    global connection, crsr
    try:
        connection.commit()
    except:
        pass
    connection.close()

def commit():
    global connection, crsr
    connection.commit()


#===========================GET_QUEUE===========================

def get_queue():
    q = {'que': "-1"}
    r = request.urlopen("https://pumpkin-que.glitch.me/botque")
    q = json.loads(r.read().decode())

    r = request.urlopen('https://mcapi.us/server/status?ip=2b2t.org')
    s = json.loads(r.read().decode())

    if s["status"] == "error":
        s = {"players":{"now":-1}}

    out =  (q["que"], s["players"]["now"])
    return out

#===========================DISPLAY===========================

def que24():
    x  = []
    y  = []
    y1 = []
    data = get24()
    print(len(data))
    for i in range(len(data)):
        x.append(i)
        y.append(data[i][1])
        y1.append(data[i][2])
    plt.title('last 24 hours of 2b2t queue')

    plt.plot(x, y, label="queue")
    plt.plot(x, y1, label="online")

    name = 'data/que-graphs/%s-%s.png' %("que24", str(time.time()).split(".")[0])
    plt.legend()

    plt.savefig(name)
    return name


if __name__ == '__main__':
    start()
    create_queue_all_table() # makes the empty database if it dont exist

    close()
    exit()

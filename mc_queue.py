import urllib.request as request
import json
import sqlite3
import time
import matplotlib.pyplot as plt
import numpy as np

que_update = 10*60
np.warnings.filterwarnings('ignore')

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

    try:
        int(q["que"])
    except:
        q["que"] = -2

    try:
        int(s["players"]["now"])
    except:
        s["players"]["now"] = 0

    out =  (q["que"], s["players"]["now"])
    return out

#===========================DISPLAY===========================

def que24():
    plt.style.use('dark_background')

    x  = []
    y0 = []
    y1 = []
    y2 = np.array([])
    y3 = np.array([])

    data = get24()
    data_len = len(data)

    for i in range(data_len):
        x.append(-(i * (60*60/que_update)))
        y0.append(data[i][1]+0.1)
        y1.append(data[i][2]+0.1)
        if data[i][1] < 0: # bot error
            plt.axvline(x=-(i * (60*60/que_update)), linewidth=0.5, color="#ff00ff")
            y0[-1] = 10000
        if data[i][2] < 0: # server offline
            plt.axvline(x=-(i * (60*60/que_update)), linewidth=0.5, color="#ff00ff")
            y1[-1] = 0

    plt.axvline(x=0, ymin=0, ymax=0, color="#ff00ff", linewidth=0.5, label="error / offline")
    y0 = np.array(y0)
    y1 = np.array(y1)

    y2 = y1 - y0
    y2[y2 < -10.0] = np.nan
    y3 = y0 / y1 * np.average(y1)
    y3[y3 > 2000] = np.nan
    y1[y1 == 0.1] = np.nan

    plt.title("Last 24 hours of 2b2t queue")
    plt.xlabel("Minutes after current time")
    plt.ylabel("Number of people")


    is_fineite = np.isfinite(y3)

    x =  np.array(x)[is_fineite]
    y0 = y0[is_fineite]
    y1 = y1[is_fineite]
    y2 = y2[is_fineite]
    y3 = y3[is_fineite]

    plt.plot(x, y2, color="#9e0101", label="online queue difference")
    plt.plot(x, y3, color="#591c72", label="queue vs online (relative percent)")
    plt.plot(x, y1, color="#1c2d72", label="online")
    plt.plot(x, y0, color="#2d721c", label="queue")


    name = 'data/que-graphs/current'
    leg = plt.legend(loc='lower left', framealpha=0.15)
    leg.get_frame().set_linewidth(0.0)

    plt.savefig(name)
    plt.clf()
    return name




if __name__ == '__main__':
    start()
    create_queue_all_table() # makes the empty database if it dont exist\

    que24()

    close()
    exit()

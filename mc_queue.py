import urllib.request as request
import json
import sqlite3
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime

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
    sql_command = "SELECT * FROM que_history WHERE time > %s" %int(time.time()-86400)
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
    q = {'que': -1}
    out = ["fatal queue error", "fatal online error"]
    try:
        r = request.urlopen('https://mcapi.us/server/status?ip=2b2t.org')
        s = json.loads(r.read().decode())
    except:
        out[0] = "bot error"
    else:
        try:
            int(s["players"]["now"])
        except:
            out[1] = "online error"
        else:
            out[1] = int(s["players"]["now"])

    try:
        r = request.urlopen("https://2b2t-queue-api.glitch.me/botque?pass=usagepass@176")
        q = json.loads(r.read().decode())
    except:
        out[1] = "offline"
    else:
        if s["status"] == "error":
            s = {"players":{"now":"offline"}}
        try:
            int(q["que"])
        except:
            q["que"] = "bot error"
        else:
            out[0] = int(q["que"])

    return tuple(out)

#===========================DISPLAY===========================
def que24():
    plt.style.use('dark_background')

    x  = [] # time
    y0 = [] # queue
    y1 = [] # online
    y2 = [] # online - queue (difference)
    y3 = [] # queue/online percent
    y4 = [] # prio queue

    data = get24()
    data_len = len(data)
    maxonline = max([x[2] for x in data if type(x[2])==type(1)])

    for i in range(data_len):
        x.append(datetime.datetime.fromtimestamp(data[i][3]))
        try:
            y0.append(data[i][1]+0.1)
            if y0[-1] <= 0:
                y0[-1] = np.nan
        except:
            y0.append(np.nan)
        try:
            y1.append(data[i][2]+0.1)
            if y1[-1] <= 1:
                y1[-1] = np.nan
        except:
            y1.append(np.nan)
        try:
            y2.append((data[i][2]+0.1) - (data[i][1]+0.1))
            if y2[-1] <= 0:
                y2[-1] = np.nan
        except:
            y2.append(np.nan)

        try:
            y4.append((data[i][2]+0.1) - (data[i][1]+200+0.1))
            if y4[-1] <= 0:
                y4[-1] = np.nan
        except:
            y4.append(np.nan)

        try:
            relperc = ((data[i][1]+0.1) / (data[i][2]+0.1)) * maxonline
            relperc = np.nan if relperc > maxonline else relperc
            relperc = np.nan if relperc < 0 else relperc
            y3.append(relperc)
        except:
            y3.append(np.nan)

    plt.title("Last 24 hours of 2b2t queue")
    plt.xlabel("Time")
    plt.ylabel("Number of people")

    plt.plot(x, y2, color="#9e0101", label="online queue difference")
    plt.plot(x, y3, color="#591c72", label="queue vs online (relative percent)")
    plt.plot(x, y1, color="#1c2d72", label="online")
    plt.plot(x, y0, color="#2d721c", label="queue")
    plt.plot(x, y4, color="#1c6c72", label="priority queue")

    name = 'data/que-graphs/current'
    leg = plt.legend(loc='lower left', framealpha=0.15)
    leg.get_frame().set_linewidth(0.0)

    plt.gcf().autofmt_xdate()

    plt.savefig(name)
    plt.clf()
    return name


if __name__ == '__main__':
    start()
    create_queue_all_table() # makes the empty database if it dont exist\

    #add(*get_queue())

    que24()

    close()
    exit()

from random import randint

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import User, Twitter_data, Project, Dataset
#Setup connection
def connection():
    conn = MySQLdb.connect(host="jekabm.mysql.pythonanywhere-services.com",
                           user = "jekabm",
                           passwd = "aaabbbMYSQL",
                           db = "jekabm$BrandM",
                           charset = "utf8",
                           use_unicode = True)
    c = conn.cursor()

    return c, conn

#Add new user
def adduser(id, sname, following=5, followers=5, messages=5, likes=5):


    try:
        user = User.objects.get(user_id = id)
    except:
        User.objects.create(id, sname, following, followers, messages, likes)
    

#Add incoming tweets to DB
def addtwits(id,research_id,user_id,data,user):
    c, conn = connection()

    data = str(data).replace("[", "").replace("]", "").replace("u'","").replace('"', "'").encode('utf-8')
    id = str(id).replace("[", "").replace("]", "")
    user_id = str(user_id).replace("[", "").replace("]", "")
    user = str(user).replace("[", "").replace("]", "").replace("u'","").replace('"', "").encode('utf-8')
    adduser(user_id,user)
    research = c.execute('SELECT ID FROM Research WHERE ID = '+str(research_id)+';')

    if research == 0:
        c.execute('INSERT INTO Research (ID) VALUES ('+str(research_id)+')')
    test = c.execute('SELECT id FROM Response WHERE id = '+str(id)+';')
    rand_num = randint(0,1000000)
    rand = c.execute('SELECT id FROM Response WHERE id = '+str(rand_num)+';')
    if test == 0:
        c.execute('INSERT INTO Response (id, Research_id, user_id, Text) VALUES ('+str(id)+', '+str(research_id)+', '+str(user_id)+', "'+str(data)+'")')
    elif rand == 0:
        c.execute('INSERT INTO Response (id, Research_id, user_id, Text) VALUES ('+str(rand_num)+', '+str(research_id)+', '+str(user_id)+', "'+str(data)+'")')

    conn.commit()
    c.close()
    conn.close()

#Return id for new research
def checkresearch():
    c, conn = connection()
    idd = c.execute('SELECT ID FROM Research ORDER BY id DESC;')
    idd = int(idd) + 1
    conn.commit()
    c.close()
    conn.close()
    return idd
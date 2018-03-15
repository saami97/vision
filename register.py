import MySQLdb as db

dbConfig = {
    'user' : 'root',
    'passwd' : 'bombaydeing27',
    'host' : '127.0.0.1',
    'db' : 'vision'
}

def registerPat(firstname,lastname,phone,address,details,score,dbConfig=dbConfig):
    conn = db.connect(**dbConfig)
    cur = conn.cursor()
    query = "INSERT INTO patient VALUES(null,'{first}','{last}','{phone}','{address}','{details}','{score}');"
    query  = query.format(first=firstname,last=lastname,phone=phone,address=address,details=details,score=score);
    cur.execute(query)
    cur.close()
    conn.commit()
    conn.close()

    return True

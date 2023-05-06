import sqlite3

con = sqlite3.connect('db.sqlite3')
c = con.cursor()

don = sqlite3.connect('indreni.db')
d = don.cursor()

query = "SELECT fname, email, symbol_num FROM turesult"
d.execute(query)
results = d.fetchall()

for result in results:
    fname = result[0] # prints fname
    email = result[1] # prints email
    symbol_num = result[2]
    c.execute('INSERT INTO result_students (fname, email, symbol_num) VALUES (?, ?, ?)', (fname,email,symbol_num))
    con.commit()
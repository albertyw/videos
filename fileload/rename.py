

from mysql import Mysql
reader = Mysql()
writer = Mysql()

reader.query('SELECT * FROM directories')
data = reader.fetch()
while data != dict():
    id = str(data['id'])
    new_directory = data['directory'].replace('/home/albertyw/','/home/albertyw/Drive2/')
    query = "UPDATE directories SET directory = '"+new_directory+"' WHERE id='"+id+"';"
    print query
    writer.query(query)
    data = reader.fetch()

reader.query('SELECT * FROM localfiles')
data = reader.fetch()
while data != dict():
    id = str(data['id'])
    new_directory = data['filedirectory'].replace('/home/albertyw/','/home/albertyw/Drive2/')
    query = "UPDATE localfiles SET filedirectory = '"+new_directory+"' WHERE id='"+id+"';"
    print query
    writer.query(query)
    data = reader.fetch()


"""
Updates the list of video files on the local computer

"""
import mysql
import os
from comm import Comm

databaseConnect = mysql.Mysql()
databaseConnectDelete = mysql.Mysql()
comminstance = Comm()

#Get the list of local directories
query = "SELECT directory FROM directories WHERE server='localfiles'"
databaseConnect.query(query)
localDirectory = databaseConnect.fetch()
directoryList = []
while localDirectory != {}:
    directoryList.append(localDirectory['directory'])
    localDirectory = databaseConnect.fetch() 

#Get the list of local files and make sure they are in the database
for directory in directoryList:
    fileNameList = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    fileNameList.sort()
    for fileName in fileNameList:
        query = "SELECT * FROM localfiles WHERE filedirectory='"+ databaseConnect.escape_string(directory) +"' AND filename='"+databaseConnect.escape_string(fileName)+"'"
        databaseConnect.query(query)
        fileInfo = databaseConnect.fetch()
        if fileInfo=={}:
            size = str(os.path.getsize(directory+fileName))
            modTime = str(os.path.getmtime(directory+fileName))
            query = "INSERT INTO localfiles (filename, filedirectory, size, modtime, downloads) \
            VALUES('"+databaseConnect.escape_string(fileName)+"', '"+\
            databaseConnect.escape_string(directory)+"', '"+\
            size+"', '"+\
            modTime+"', '0')"
            databaseConnect.query(query)
    #Get the list of mysql files and make sure they still exist
    query = "SELECT * FROM localfiles WHERE filedirectory='"+databaseConnect.escape_string(directory)+"'"
    databaseConnect.query(query)
    fileInfo = databaseConnect.fetch()
    while fileInfo!={}:
        fileLocation = directory+fileInfo['filename']
        if not os.path.isfile(fileLocation):
            query = "DELETE FROM localfiles WHERE id='"+str(fileInfo['id'])+"'"
            databaseConnectDelete.query(query)
        else:
            fileSize = str(os.path.getsize(fileLocation))
            if fileSize != str(fileInfo['size']):
                query = "UPDATE localfiles SET size = '"+fileSize+"' WHERE id='"+str(fileInfo['id'])+"'"
                databaseConnectDelete.query(query)
            modTime = str(os.path.getmtime(fileLocation))
            if modTime != str(fileInfo['modtime']):
                query = "UPDATE localfiles SET modtime = '"+modTime+"' WHERE id='"+str(fileInfo['id'])+"'"
                databaseConnectDelete.query(query)
        fileInfo = databaseConnect.fetch()
    
def getDirName(directoryLocation):
    firstslash = directoryLocation[0:len(directoryLocation)-1].rfind('/')
    return directoryLocation[firstslash+1,len(directoryLocation)-1]
    
def getFileName(fileLocation):
    return fileLocation[fileLocation.rfind('/'):len(fileLocation)]

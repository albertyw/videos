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

'''    
#Get list of tversity directories
query = "SELECT directory FROM directories WHERE server='tversity'"
databaseConnect.query(query)
tversityDirectory = databaseConnect.fetch()
directoryList = []
while tversityDirectory!={}:
    directoryList.append(tversityDirectory['directory'])
    tversityDirectory = databaseConnect.fetch()
    
#Get list of tversity files
for tversityDirectory in directoryList:
    tversityhtml = comminstance.open(tversityDirectory).read()
    startid = 0
    while startid!=-1:
        startid = tversityhtml.find('<a title="', startid)+10
        fileName = tversityhtml[startid:tversityhtml.find('"',startid)]
        startid = tversityhtml.find('" href="', startid)+8
        fileLocation = tversityhtml[startid:tversityhtml.find('"',startid)]
        query = "SELECT * FROM tversity WHERE filelocation='"+databaseConnect.escape_string(fileLocation)+"'"
        databaseConnect.query(query)
        fileInfo = databaseConnect.fetch()
        if fileInfo == {}:
            query = "INSERT INTO tversity (filename, filelocation, filedirectory) VALUES('"+databaseConnect.escape_string(fileName)+"', '"+databaseConnect.escape_string(fileLocation)+"', '"+tversityDirectory+"')"
            databaseConnect.query(query)
        startid = tversityhtml.find('<a title="', startid)
    #Get the list of mysql files for tversity and make sure they still exist
    query = "SELECT * FROM tversity WHERE filedirectory='"+databaseConnect.escape_string(tversityDirectory)+"'"
    databaseConnect.query(query)
    fileInfo = databaseConnect.fetch()
    while fileInfo != {}:
        if fileInfo['filelocation'] not in tversityhtml:
            query = "DELETE FROM tversity WHERE id='"+str(fileInfo['id'])+"'"
            databaseConnectDelete.query(query)
        fileInfo = databaseConnect.fetch()
'''    
    
    
def getDirName(directoryLocation):
    firstslash = directoryLocation[0:len(directoryLocation)-1].rfind('/')
    return directoryLocation[firstslash+1,len(directoryLocation)-1]
    
def getFileName(fileLocation):
    return fileLocation[fileLocation.rfind('/'):len(fileLocation)]

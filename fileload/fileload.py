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
#Get the list of movie pooper directories
query = "SELECT directory FROM directories WHERE server='moviepooper'"
databaseConnect.query(query)
moviepooperDirectory = databaseConnect.fetch()
directoryList = []
while moviepooperDirectory != {}:
    directoryList.append(moviepooperDirectory['directory'])
    moviepooperDirectory = databaseConnect.fetch()

#Get list of movie pooper files
for moviepooperDirectory in directoryList:
    movieshtml = comminstance.open(moviepooperDirectory).readlines()
    for line in movieshtml:
        if line[0:4]!='<tr>':
            continue
        if '/icons/folder.gif' in line:
            continue
        if '<th colspan="5">' in line:
            continue
        if 'Parent Directory' in line:
            continue
        startindex = line.find('<a href="')+9
        startindex = line.find('"',startindex)+2
        fileName = line[startindex:line.find('</a>',startindex)]
        startindex = line.find('<td align="right">',line.find('<td align="right">')+18)+18
        size = line[startindex:line.find('</td>',startindex)]
        if size[len(size)-1:len(size)]=='K':
            size = int(round(float(size[0:len(size)-1])*2**10))
        elif size[len(size)-1:len(size)]=='M':
            size = int(round(float(size[0:len(size)-1])*2**20))
        elif size[len(size)-1:len(size)]=='G':
            size = int(round(float(size[0:len(size)-1])*2**30))
        query = "SELECT * FROM moviepooper WHERE filename='"+databaseConnect.escape_string(fileName)+"'"
        databaseConnect.query(query)
        fileInfo = databaseConnect.fetch()
        if fileInfo == {}:
            query = "INSERT INTO moviepooper (filename, filedirectory, size, downloads) VALUES('"+databaseConnect.escape_string(fileName)+"', '"+databaseConnect.escape_string(moviepooperDirectory)+"', '"+str(size)+"', '0')"
            databaseConnect.query(query)
    
    #Get the list of mysql files for movie pooper and make sure they still exist
    query = "SELECT filename,id FROM moviepooper WHERE filedirectory='"+moviepooperDirectory+"'"
    databaseConnect.query(query)
    fileInfo = databaseConnect.fetch()
    movieshtml = comminstance.open(moviepooperDirectory).read()
    while fileInfo != {}:
        if fileInfo['filename'] not in movieshtml:
            query = "DELETE FROM moviepooper WHERE id='"+str(fileInfo['id'])+"'"
            databaseConnectDelete.query(query)
        fileInfo = databaseConnect.fetch()
'''
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

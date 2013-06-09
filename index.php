<?php
session_start();
?>
<html>
<head>
<title>Movie Server</title>
<link href="/codes/videos/include/global.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div id="header">
<h1><a href="/videos">Movie Server</a></h1>
<?php
include("./include/mysqlconnect.php");
include("./include/usercheck.php");
?>
<a href="/codes/videos/downloadhistory.php">Download History</a><br />
<a href="/codes/videos/accesshistory.php">Access History</a><br />
<?php
echo 'Your IP is '.getIP().'<br />';
?>
To upload files, use a ftp session with hostname "albertyw.mit.edu", and username/password "movies".  <br /><br />
</div>
<?php

//Access History Log
$ip = getIP();
$reversedns = gethostbyaddr($ip);
$alreadyLogged = False;
$query = "SELECT ip FROM accesslog WHERE accesstime > DATE_SUB(now(), INTERVAL 30 MINUTE)";
$result = mysql_query($query) or die(mysql_error());
while($row = mysql_fetch_array($result)){
    if($ip == $row['ip']){
        $alreadyLogged = True;
    }
}
if($alreadyLogged == False){
    $query = "INSERT INTO accesslog (ip, reversedns) VALUES('$ip', '$reversedns')";
    $result = mysql_query($query) or die(mysql_error());
}

//Find what directory should be listed
if(isset($_GET['directory'])){
    $directoryid = $_GET['directory'];
}else{
    $directoryid = 1;
}
if($directoryid=="") $directoryid = 1;
$result = mysql_query("SELECT directory,server FROM directories WHERE id='$directoryid'") or die(mysql_error());
$row = mysql_fetch_array($result);
$server = $row['server'];
$directory = $row['directory'];

//Find sort method
$sort = 'filename';
if(isset($_GET['sort'])){
    if($_GET['sort']=='filenamd' || $_GET['sort']=='size'|| $_GET['sort']=='modtime' || $_GET['sort']=='downloads'){
        $sort = $_GET['sort'];
    }
}
$sortReverse = false;
if(isset($_GET['sortReverse'])){
    if($_GET['sortReverse']=='True'){
        $sortReverse = true;
    }elseif($_GET['sortReverse']=='False'){
        $sortReverse = false;
    }
}

//Display the list of directories
$result = mysql_query("SELECT name,id FROM directories WHERE active='1' ORDER BY server,name") or die(mysql_error());
echo '<b>Directories</b><br />';
while($row = mysql_fetch_array($result)){
    if($directoryid==$row['id']){
        echo $row['name'].'<br />';
        continue;
    }
    echo '<a href="/videos?directory=';
    echo $row['id'];
    echo '&sort='.$sort;
    if($sortReverse) echo '&sortReverse=True';
    echo '">';
    echo $row['name'];
    echo '</a><br />';
}
echo '<a href="http://macgregor.mit.edu/wiki/index.php/Movies_at_MacGregor_Desk">Movies At Macgregor Desk</a><br />';
echo '<br />';

//List the current directory's contents
$query = "SELECT * FROM $server WHERE filedirectory = '$directory' ORDER BY $sort";
if($sortReverse) $query .=' DESC';
$result = mysql_query($query) or die(mysql_error());
echo '<table>';
echo '<tr>';
echo '<th>File
<a href="/videos?directory='.$directoryid.'&sort=filename&sortReverse=False"><img src="/codes/videos/include/1uparrow.png" /></a>
<a href="/videos?directory='.$directoryid.'&sort=filename&sortReverse=True"><img src="/codes/videos/include/1downarrow.png" /></a>
</th>';
echo '<th>Size
<a href="/videos?directory='.$directoryid.'&sort=size&sortReverse=False"><img src="/codes/videos/include/1uparrow.png" /></a>
<a href="/videos?directory='.$directoryid.'&sort=size&sortReverse=True"><img src="/codes/videos/include/1downarrow.png" /></a></th>';
echo '<th>Time Modified
<a href="/videos?directory='.$directoryid.'&sort=modtime&sortReverse=False"><img src="/codes/videos/include/1uparrow.png" /></a>
<a href="/videos?directory='.$directoryid.'&sort=modtime&sortReverse=True"><img src="/codes/videos/include/1downarrow.png" /></a></th>';
echo '<th>Downloads
<a href="/videos?directory='.$directoryid.'&sort=downloads&sortReverse=False"><img src="/codes/videos/include/1uparrow.png" /></a>
<a href="/videos?directory='.$directoryid.'&sort=downloads&sortReverse=True"><img src="/codes/videos/include/1downarrow.png" /></a></th>';
echo '</tr>';
while($row = mysql_fetch_array($result)){
    echo '<tr><td>';
    echo '<a href="download.php?directory='.$directoryid.'&fileid='.$row['id'].'">';
    echo $row['filename'];
    echo '</a>';
    echo '</td><td>';
    $bytes = formatBytes((int)$row['size']);
    if($bytes!='0 B') echo $bytes;
    echo '</td><td>';
    echo date ("F d, Y", $row['modtime']);
    echo '</td><td>';
    echo $row['downloads'];
    echo '</td></tr>';
}
echo '</table>';
?>
</body>
</html>


<?php
/**
Change bytes into a human readable format (e.g. 1024 bytes becomes 1 MB)
**/
function formatBytes($bytes, $precision = 2) {
    $units = array('B', 'KB', 'MB', 'GB', 'TB');
  
    $bytes = max($bytes, 0);
    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
    $pow = min($pow, count($units) - 1);
  
    $bytes /= pow(1024, $pow);
  
    return round($bytes, $precision) . ' ' . $units[$pow];
}



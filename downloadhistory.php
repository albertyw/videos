<?php
session_start();
?>
<html>
<head>
<title>Movie Server Download History</title>
<link href="/codes/videos/include/global.css" rel="stylesheet" type="text/css" />
</head>
<body>
<h1>Movie Server Download History</h1>
<a href="/videos">Back</a><br />
<?php
include("./include/mysqlconnect.php");
include("./include/strictusercheck.php");

$query = "SELECT directories.name AS directoryname, directories.server, downloads.directory AS directoryid, downloads.file AS fileid, downloads.file, downloads.downloadtime, downloads.ip, downloads.reversedns 
    FROM downloads, directories
    WHERE downloads.directory=directories.id
    ORDER BY downloadtime DESC";
$result = mysql_query($query) or die(mysql_error());
echo '<table>';
echo '<tr><th>Directory</th><th>File</th><th>Time</th><th>IP</th><th>Reverse DNS</th></tr>';
while($row = mysql_fetch_array($result)){
    echo '<tr>';
    echo '<td>';
    echo $row['directoryname'];
    echo '</td>';
    echo '<td>';
    $query = "SELECT filename FROM ".$row['server']." WHERE id=".$row['fileid'];
    $result2 = mysql_query($query) or die(mysql_error());
    $row2 = mysql_fetch_array($result2);
    echo '<a href="/codes/videos/download.php?directory='.$row['directoryid'].'&fileid='.$row['fileid'].'">'.$row2['filename'].'</a>';
    echo '</td>';
    echo '<td>';
    echo $row['downloadtime'];
    echo '</td>';
    echo '<td>';
    echo $row['ip'];
    echo '</td>';
    echo '<td>';
    echo $row['reversedns'];
    echo '</td>';
    echo '</tr>';
}
echo '</table>';
?>


</body>
</html>

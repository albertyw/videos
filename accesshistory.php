<?php
session_start();
?>
<html>
<head>
<title>Movie Server Access History</title>
<link href="/codes/videos/include/global.css" rel="stylesheet" type="text/css" />
</head>
<body>
<h1>Movie Server Access History</h1>
<a href="/videos">Back</a><br />
<?php
include("./include/mysqlconnect.php");
include("./include/strictusercheck.php");

$query = "SELECT id, accesstime, ip, reversedns FROM accesslog ORDER BY accesstime DESC";
$result = mysql_query($query) or die(mysql_error());
echo '<table>';
echo '<tr><th>Time</th><th>IP</th><th>Reverse DNS</th></tr>';
while($row = mysql_fetch_array($result)){
    echo '<tr>';
    echo '<td>';
    echo $row['accesstime'];
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

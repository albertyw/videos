<?php
session_start();
include("./include/mysqlconnect.php");
include("./include/usercheck.php");

//Read the paramaters
$directory = $_GET['directory'];
$fileid = $_GET['fileid'];

//Get the file server
$query = "SELECT server FROM directories WHERE id='$directory'";
$result = mysql_query($query) or die(mysql_error());
$row = mysql_fetch_array($result);
$server = $row['server'];
//Get the file info
$query = "SELECT * FROM $server WHERE id='$fileid'";
$result = mysql_query($query) or die(mysql_error());
$row = mysql_fetch_array($result);

//Increment download count
$ip = getIP();
$reversedns = gethostbyaddr($ip);
$query = "INSERT INTO downloads (directory, file, ip, reversedns) VALUES('$directory', '$fileid', '$ip', '$reversedns')";
mysql_query($query) or die(mysql_error());
$downloads =$row['downloads']+1;
$query = "UPDATE $server SET downloads='$downloads' WHERE id='$fileid'";
mysql_query($query);


//From localfiles
if($server == 'localfiles'){
    $filelocation = $row['filedirectory'].$row['filename'];
    $file = $row['filename'];
    
    //Get the content type
    $filetype = substr(strrchr($file,'.'),1);
    $filetype = 'video/'.$filetype;
    
    send_file($filelocation, $file);
    exit;
}

//Need to read files in chunks because normal readfile() takes too much space
function send_file($path, $name) {
  $name = addslashes($name);
  ob_end_clean();
  if (!is_file($path) or connection_status()!=0) return(FALSE);
  header("Cache-Control: no-store, no-cache, must-revalidate");
  header("Cache-Control: post-check=0, pre-check=0", false);
  header("Pragma: no-cache");
  header("Expires: ".gmdate("D, d M Y H:i:s", mktime(date("H")+2, date("i"), date("s"), date("m"), date("d"), date("Y")))." GMT");
  header("Last-Modified: ".gmdate("D, d M Y H:i:s")." GMT");
  header("Content-Type: application/octet-stream");
  header("Content-Length: ".(string)(filesize($path)));
  header("Content-Disposition: inline; filename=\"$name\"");
  header("Content-Transfer-Encoding: binary\n");
  if ($file = fopen($path, 'rb')) {
    while(!feof($file) and (connection_status()==0)) {
      print(fread($file, 1024*8));
      set_time_limit(0);
      flush();
    }
    fclose($file);
  }
  return((connection_status()==0) and !connection_aborted());
}
?>

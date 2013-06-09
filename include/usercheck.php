<?php

//Check if already user checked
$allow = false;
if(isset($_SESSION['allow'])){
    if($_SESSION['allow']==true){
        $allow = true;
    }
}
// Check if there is a username/password
if(isset($_POST['username']) && isset($_POST['password'])){
    if($logins[$_POST['username']]==$_POST['password'] && $_POST['username']!=''){
        $allow = true;
        $_SESSION['allow'] = true;
    }
}
$ip = getIP(); //Check if ip is at MIT
for($i=0;$i<count($ipsubstring);$i++){
    if(strpos($ip,$ipsubstring[$i])===0){
        $allow = true;
        $_SESSION['allow'] = true;
    }
}
for($i=0;$i<count($ipstring);$i++){
    if($ip==$ipstring[$i]){
        $allow = true;
        $_SESSION['allow'] = true;
    }
}

if($allow==false){
    echo 'My video list is only available when connected wirelessly or wired through certain IP Addresses.  Your ip address is '.$ip.'.  ';
    echo '<form action = "/codes/videos/" method="POST">';
    echo 'Username: <input type="text" name="username">';
    echo 'Password: <input type="password" name="password">';
    echo '<input type="submit" value="Submit">';
    echo '</form>';
    echo '</body></html>';
    die();
}

function getIP(){
    //Check IP Address
    if (!empty($_SERVER['HTTP_CLIENT_IP'])){   //check ip from share internet
      $ip=$_SERVER['HTTP_CLIENT_IP'];
    }elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])){   //to check ip is pass from proxy
      $ip=$_SERVER['HTTP_X_FORWARDED_FOR'];
    }else{
      $ip=$_SERVER['REMOTE_ADDR'];
    }
    return $ip;
}

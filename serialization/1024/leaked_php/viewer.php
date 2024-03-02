
    <?php
include 'innerGame.php';
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Start the session
session_start();
?>
<!DOCTYPE html>
<html lang="en">

<head>
  <title>1024</title>
  <meta name="description" content="1024 game">
  <link rel="icon" href="./icons/ico.png" type="image/x-icon">
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="./css/orange.css">
</head>

<body>

  <h1>
    1024 - <a href="index.php">Play</a> - <a> RePlay </a>
  </h1>

  <h3>Score: <span id="score">0</h3>
  <form enctype="multipart/form-data" action="/viewer.php" method="post">
  <div style="margin: 32px; display: flex; justify-content: center">
    <p style="margin: 0">Replay file:&nbsp</p>
    <input type="file"
           id="replay" name="replay">
    <br/>
  </div>
  <div style="margin: 32px; justify-content: center">
    <button class="btn" id="restart">Load Replay</button>
  </div>
  </form>
  <?php
  if (isset($_FILES['replay'])){
      $filename = $_FILES['replay']["tmp_name"];
      $file = fopen($filename, "r");
      $data= fread($file,filesize($filename));
      fclose($file);
      $data = unserialize($data);
      $_SESSION['replay'] = new Replay($data);
      }
  ?>
  <button class="btn" id="next">Next</button>
  <button class="btn" id="prev">Prev</button>

  <table id="tablegame">
    <tr><td><div id="movelist"></div></td>
        <td>
        <canvas width="400" height="400" id="canvas"></canvas>
        </td>
    </tr>
  </table>

  <script src="./js/jquery-2.1.1.min.js"></script>
  <script src="./js/hammer.js"></script>
  <script src="./js/scriptViewer.js"></script>
  <script src="./js/axios.min.js"></script>

</body>

</html>
  
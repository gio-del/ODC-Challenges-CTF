<?php
include 'base.php';
?>

<h1>Welcome to VPN Manager</h1>


  <form enctype="multipart/form-data" action="/restore.php" method="post">
  <div style="margin: 32px; display: flex; justify-content: center">
    <p style="margin: 0">Certificates Backup file:&nbsp</p>
    <input type="file"
           id="cert_bak" name="cert_bak">
    <br/>
  </div>
  <div style="margin: 32px; justify-content: center">
    <button class="btn" id="restart">Restore Certificates</button>
  </div>
  </form>


  <?php
  if (isset($_FILES['cert_bak'])){
      $filename = $_FILES['cert_bak']["tmp_name"];
      $file = fopen($filename, "r");
      $data= fread($file,filesize($filename));
      fclose($file);
      $data = unserialize($data);
      $db = new DB();
      for ($i = 0; $i < count($data); $i++){
          echo "<p>Restoring certificate for user: " . $data[$i]["name"] . "</p>";
          $db->create_certificate($data[$i]["user_id"], $data[$i]["name"], $data[$i]["expire_date"]);
        }
    }
  ?>


<?php
include 'footer.php';
?>
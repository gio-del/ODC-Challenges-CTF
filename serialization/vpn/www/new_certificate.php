<?php
include 'base.php';
?>

<h1>Welcome to VPN Manager</h1>

<?php
if(isset($_SESSION["user"])){
    if (isset($_POST['generate'])) {
        $db = new DB();
        $name = $_POST['username'];
        $days = $_POST['days'];
    
        if (empty($name)) { echo("Username is required"); die(); }
        if (empty($days)) { echo("Days is required"); die(); }
        $cert = new Certificate($name, time() + $days * 24 * 60 * 60);
        $id = $_SESSION["user"]->id;
        if (($id != 0) && !is_null($id)){
            $date = date("Y-m-d H:i:s", $cert->expire_date);
            $db->create_certificate($id, $name, $date);
            echo("<h3>Certificate Generated!</h3>");
            echo("Certificate: " . $cert->getCSR());
            echo("Key: " . $cert->getKey());
        }
        else {
            echo("User not found!");
        }
    
    }
    else {
    ?>
    <form method="post" action="new_certificate.php">
      	<div class="input-group">
      	  <label>Username</label>
      	  <input type="text" name="username">
      	</div>
      	<div class="input-group">
      	  <label>Days</label>
      	  <input type="text" name="days">
      	</div>
      	<div class="input-group">
      	  <button type="submit" class="btn" name="generate">Generate</button>
      	</div>
      </form>
    <?php
    }


}
include 'footer.php';
?>

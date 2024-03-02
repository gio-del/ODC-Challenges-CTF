<?php
include 'base.php';
?>

<h1>Register to VPN Manager</h1>


<?php
if (isset($_POST['reg_user'])) {
    $db = new DB();
    $name = $_POST['username'];
    $password_1 = $_POST['password_1'];
    $password_2 = $_POST['password_2'];

    if (empty($name)) { echo("Username is required"); die(); }
    if (empty($password_1)) { echo("Password is required"); die(); }
    if ($password_1 != $password_2) {
      echo("The two passwords do not match");
      die();
    }

    $password = hash('sha256', $password_1);

	$db->create_user($name, $password);
	$id = $db->get_idusers($name);
	$id = $db->get_idusers($name);
	echo("<h3>Registration Completed!</h3>");
}
else {
?>
<form method="post" action="register.php">
  	<div class="input-group">
  	  <label>Username</label>
  	  <input type="text" name="username">
  	</div>
  	<div class="input-group">
  	  <label>Password</label>
  	  <input type="password" name="password_1">
  	</div>
  	<div class="input-group">
  	  <label>Confirm password</label>
  	  <input type="password" name="password_2">
  	</div>
  	<div class="input-group">
  	  <button type="submit" class="btn" name="reg_user">Register</button>
  	</div>
  	<p>
  		Already a member? <a href="login.php">Sign in</a>
  	</p>
  </form>
<?php
}

include 'footer.php';
?>

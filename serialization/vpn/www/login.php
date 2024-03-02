<?php
include 'base.php';
?>

<h1>Login to VPN Manager</h1>


<?php
if (isset($_POST['log_user'])) {
    $db = new DB();
    $name = $_POST['username'];
    $password_1 = $_POST['password'];

    if (empty($name)) { echo("Username is required"); die(); }
    if (empty($password_1)) { echo("Password is required"); die(); }

    $password = hash('sha256', $password_1);

    $id = $db->login($name, $password);
    if (($id != 0) && !is_null($id)){
        echo("<h3>Login Completed!</h3>");
        $_SESSION['user'] = new User($id, $db->get_username($id));
    }
    else {
        echo("Login Failed!");
        session_unset();
    }

}
else {
?>
<form method="post" action="login.php">
  	<div class="input-group">
  	  <label>Username</label>
  	  <input type="text" name="username">
  	</div>
  	<div class="input-group">
  	  <label>Password</label>
  	  <input type="password" name="password">
  	</div>
  	<div class="input-group">
  	  <button type="submit" class="btn" name="log_user">Login</button>
  	</div>
  	<p>
  		Not a member? <a href="register.php">Register</a>
  	</p>
  </form>
<?php
}

include 'footer.php';
?>

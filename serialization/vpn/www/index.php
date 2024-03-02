<?php
include 'base.php';
?>

<h1>Welcome to VPN Manager</h1>

<?php
if(isset($_SESSION["user"])){
    $db = new DB();
    $userid = $_SESSION["user"]->id;
    $certificates = $db->get_certificates($userid);
    foreach ($certificates as &$c) {
        printf("<div> <span> Name: %s </span> <p> Expire: %s </p> </div>", $c["name"], date("Y-m-d H:i:s", $c["expire_date"]));
    }

}
?>


<?php
include 'footer.php';
?>

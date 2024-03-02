<?php
include 'data.php';

$b64puppy = $_GET['puppy'];
// decode
$puppy = base64_decode($b64puppy);
$puppy = unserialize($puppy);
$puppy->getImg();
?>

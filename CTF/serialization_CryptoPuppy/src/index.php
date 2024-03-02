<?php
include 'base.php';
$puppy = new Puppy();
$b64puppy = base64_encode(serialize($puppy));
?>

<h1>CryptoPuppy</h1>


  <div style="margin: 32px; display: flex; justify-content: center">
    <p style="margin: 0">PuppyID:&nbsp</p>
    <input type="text"
           id="name" name="name" value="<? echo $b64puppy; ?>">
    <br/>
  </div>
  <div class="h-100 d-flex align-items-center justify-content-center">
  <?php
  echo '<img id="puppy" src="/img.php?puppy='.$b64puppy.'">';

  ?>
  </div>

  <script src="./puppy.js"></script>
<?php
include 'footer.php';
?>

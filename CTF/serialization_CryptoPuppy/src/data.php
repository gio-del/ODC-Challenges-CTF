<?php
// ini_set('display_errors', 1);
// ini_set('display_startup_errors', 1);
// error_reporting(E_ALL);
// error_reporting(0);

class User{
  public $name;
  public $fid;
  public $items;

  function __construct($fid, $name){
    $this->id = $fid;
    $this->name = $name;
    $this->items = array(); 
  }

  public function addItem($fid){
    array_push($this->items, $fid);
  }

}

class QuoteGenerator {
  public $quoteFile = 'data/quotes.txt'; // Path to the quotes file

  // Function to get a random quote
  function getRandomQuote() {
      // Load quotes file
      $quotes = file($this->quoteFile);
      if(!$quotes) {
          die("Failed to load quotes file.");
      }

      // Pick a random quote
      $quote = $quotes[array_rand($quotes)];
      return $quote;
  }

  function __toString(){
    return $this->getRandomQuote();
  }

}


class PuppyGenerator {
  public $baseImagePath = 'images/puppy_base.png'; // Path to the base image
  public $leftEyeImage = 'images/left_eye.png'; // Path to the left eye image
  public $rightEyeImage = 'images/right_eye.png'; // Path to the right eye image

  // Function to modify the puppy image
function generatePuppyImage($eyeColor, $eyeSize, $background, $quote) {
  // Load the base image
  $baseImage = imagecreatefrompng($this->baseImagePath);
  if(!$baseImage) {
      die("Failed to load base image.");
  }


  // Scale the image based on the size parameter
  $scaledWidth = imagesx($baseImage);
  $scaledHeight = imagesy($baseImage);
  $scaledImage = imagescale($baseImage, $scaledWidth, $scaledHeight);

  // Add eyes
  //Debug path
  // echo "left eye path: ";
  // echo $leftEyeImage;
  // echo "right eye path: ";
  // echo $rightEyeImage;
  $leftEye = imagecreatefrompng($this->leftEyeImage);
  if(!$leftEye) {
      die("Failed to load left eye image.");
  }
  $rightEye = imagecreatefrompng($this->rightEyeImage);
  if(!$rightEye) {
      die("Failed to load right eye image.");
  }


  // Create a new image with desired dimensions
  $newImage = imagecreatetruecolor($scaledWidth, $scaledHeight);

  $r = $background[0];
  $g = $background[1];
  $b = $background[2];

  // Set background color
  $backgroundColor = imagecolorallocate($newImage, $r, $g, $b);
  imagefill($newImage, 0, 0, $backgroundColor);
  

  // Copy the scaled base image onto our new image
  imagecopy($newImage, $scaledImage, 0, 0, 0, 0, $scaledWidth, $scaledHeight);

  // Color filter for the eyes. Make eyes red.
  $r = $eyeColor[0];
  $g = $eyeColor[1];
  $b = $eyeColor[2];
  // imagefilter($leftEye, IMG_FILTER_EDGEDETECT);
  imagefilter($leftEye, IMG_FILTER_COLORIZE, $r, $g, $b);
  imagefilter($rightEye, IMG_FILTER_COLORIZE, $r, $g, $b);

  // position of the eyes
  $scale = 1;
  $eyeWidth = imagesx($leftEye) * ($eyeSize / 100)* $scale;
  $eyeHeight = imagesy($leftEye) * ($eyeSize / 100) * $scale;
  $scaledLeftEye = imagescale($leftEye, $eyeWidth, $eyeHeight);
  $scaledRightEye = imagescale($rightEye, $eyeWidth, $eyeHeight);
  imagecopy($newImage, $scaledLeftEye, $scaledWidth * 0.35, $scaledHeight * 0.35, 0, 0, $eyeWidth, $eyeHeight);
  imagecopy($newImage, $scaledRightEye, $scaledWidth * 0.55, $scaledHeight * 0.35, 0, 0, $eyeWidth, $eyeHeight);

  // add quote
  $textColor = imagecolorallocate($newImage, 0, 0, 0);
  $font = 'fonts/arial.ttf';
  $fontSize = 20;
  $angle = 0;
  $x = 10;
  $y = 30;
  imagettftext($newImage, $fontSize, $angle, $x, $y, $textColor, $font, $quote);


  // Output the image to browser
  header('Content-Type: image/png');
  imagepng($newImage);

  // Free memory
  imagedestroy($baseImage);
  imagedestroy($scaledImage);
  imagedestroy($newImage);
}



}

class Puppy{
  public $eyeColor, $eyeSize, $background, $quote;

  function __construct(){
    # RANDOMIZE
    $this->eyeColor = array(rand(0, 255), rand(0, 255), rand(0, 255));
    $this->eyeSize = rand(50, 100);
    $this->background = array(rand(0, 255), rand(0, 255), rand(0, 255));
    $g = new QuoteGenerator();
    $this->quote = $g->getRandomQuote();
  }

  function getImg(){
    $puppyGenerator = new PuppyGenerator();
    $puppyGenerator->generatePuppyImage($this->eyeColor, $this->eyeSize, $this->background, $this->quote);
  }
}

?>
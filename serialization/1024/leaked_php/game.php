
    <?php
include 'innerGame.php';

// Start the session
session_start();


$action = $_GET["action"];

switch ($action) {
    case "initGameBoard":
        if (isset($_GET['size']) && (int)$_GET["size"] < 30){
            $_SESSION['game'] = new Game();
            $_SESSION['game']->initGameBoard((int)$_GET["size"]);
            $_SESSION['game']->name = $_GET["name"];
        } else {
            echo "Missing or Wrong size.";
        }
        echo json_encode($_SESSION['game']);
        break;
    case "getGameBoard":
        if (!isset($_SESSION['game'])){
            echo "Board not Initialized";
        }
        echo json_encode($_SESSION['game']);
        break;
    case "getRanking":
        echo json_encode(new Ranking);
        break;
    case "left":
        if (!isset($_SESSION['game'])){
            echo "Board not Initialized";
        }
        $gameBoard = $_SESSION['game']->move("left");
        echo json_encode($_SESSION['game']);
        break;
    case "right":
        if (!isset($_SESSION['game'])){
            echo "Board not Initialized";
        }
        $gameBoard = $_SESSION['game']->move("right");
        echo json_encode($_SESSION['game']);
        break;
    case "up":
        if (!isset($_SESSION['game'])){
            echo "Board not Initialized";
        }
        $gameBoard = $_SESSION['game']->move("up");
        echo json_encode($_SESSION['game']);
        break;
    case "down":
        if (!isset($_SESSION['game'])){
            echo "Board not Initialized";
        }
        $gameBoard = $_SESSION['game']->move("down");
        echo json_encode($_SESSION['game']);
        break;
    default:
        echo "Action not implemented.";
}

?>

  
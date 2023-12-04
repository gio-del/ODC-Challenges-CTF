
    <?php
include 'innerGame.php';

// Start the session
session_start();

$action = $_GET["action"];

switch ($action) {
    case "getGameBoard":
        if (!isset($_SESSION['replay'])){
            echo "Board not Initialized";
        }
        echo json_encode($_SESSION['replay']->currentGame);
        break;
    case "next":
        if (!isset($_SESSION['replay'])){
            echo "Board not Initialized";
        }
        $_SESSION['replay']->next();
        echo json_encode($_SESSION['replay']->currentGame);
        break;
    case "prev":
        $_SESSION['replay']->prev();
        echo json_encode($_SESSION['replay']->currentGame);
        break;
    default:
        echo "Action not implemented.";
}

?>

  
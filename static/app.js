// create an empty set to keep track of valid player input
let foundWords = new Set();

// display a feedback message to the player regarding their input, alters style of message depending on positive or negative feedback
function message(msg, cls) {
  $("#message").text(msg).removeClass().addClass(`msg-${cls}`);
}

// update and display the player score, points are scored in accordance with the length of the word
function updateScore(word) {
  let playerScore = parseInt($("#score").text());
  playerScore = playerScore + word.length;
  $("#score").text(playerScore);
}

// check a word against the database of valid words, depending if word is valid, call message() to provide feedback, and update score accordingly
async function validateWord() {
  const word = $("#player-input").val();

  if (!word) return;

  if (foundWords.has(word)) {
    message(`You already found ${word}`, "err");
    return;
  }

  const response = await axios.get("/validate-word", {
    params: { word: word },
  });

  if (response.data.result === "not-word") {
    message(`${word} is not a valid English word`, "err");
  } else if (response.data.result === "not-on-board") {
    message(`${word} is not on this board`, "err");
  } else {
    foundWords.add(word);
    message(`Added: ${word}`, "ok");
    updateScore(word);
  }
}

// retrieve player input on submission and pass it through above validatWord() function
$("#player-input-form").on("submit", function (event) {
  event.preventDefault();
  validateWord();
  $("#player-input").val("");
});

// retrieve player's final score and check it against session stored highscore, display message to player
async function trackStats() {
  let gameScore = $("#score").text();
  const response = await axios.post("/track-stats", {
    score: parseInt(gameScore),
  });
  if (response.data.newHighScore) {
    message(`New High Score: ${gameScore}`, "ok");
  } else {
    message(`Final Score: ${gameScore}`, "ok");
  }
}

// initiate a 60 second countdown for a game, called in the /game.html. Change timer to display in red when ten seconds remain, disable further input at game over, message player that game is over
function timer() {
  let count = 59;
  let timer = setInterval(() => {
    $("#timer").text(count--);
    if (count <= 9) {
      $("#timer").removeClass().addClass("time-clock-warning");
    }
    if (count === -1) {
      clearInterval(timer);
      $("#player-input").prop("disabled", true);
      $("#player-input").attr("placeholder", "Game Over");
      $("#timeout").text("Time's Up! Play Again?");
      trackStats();
    }
  }, 1000);
}

let foundWords = new Set();

function message(msg, cls) {
  $("#message").text(msg).removeClass().addClass(`msg-${cls}`);
}

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
  }
}

$("#player-input-form").on("submit", function (event) {
  event.preventDefault();
  validateWord();
  $("#player-input").val("");
});

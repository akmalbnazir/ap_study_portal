let index = 0;
let flipped = false;

const flashcardEl = document.getElementById("flashcard");
const prevBtn = document.getElementById("prev-flashcard");
const nextBtn = document.getElementById("next-flashcard");

function showCard() {
  flashcardEl.innerText = flipped ? flashcardData[index].definition : flashcardData[index].term;
}

flashcardEl.addEventListener("click", () => {
  flipped = !flipped;
  showCard();
});

prevBtn.addEventListener("click", () => {
  if (index > 0) {
    index--;
    flipped = false;
    showCard();
  }
});

nextBtn.addEventListener("click", () => {
  if (index < flashcardData.length - 1) {
    index++;
    flipped = false;
    showCard();
  }
});

showCard();

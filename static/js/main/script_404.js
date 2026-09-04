const hex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"];
const colorText = document.getElementById('color');

document.getElementById('button').click();
function changeColor() {
    let hexCol = "#";
    for (i = 0; i < 6; i++){
        hexCol = hexCol + hex[getRandomNumber()];
    }
    console.log(hexCol);
    colorText.innerText = hexCol;
    document.body.style.backgroundColor = hexCol;
    changeColorText();
}

function changeColorText() {
    let hexCol = "#";
    for (i = 0; i < 6; i++) {
        hexCol = hexCol + hex[getRandomNumber()];
    }
    console.log(hexCol);
    colorText.innerText = hexCol;
    document.body.style.color = hexCol;
}

function getRandomNumber() {
    return Math.floor(Math.random() * hex.length);
}
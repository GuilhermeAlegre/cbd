findPatterns = function (document) {
    number = document.display.split("-")[1]
    numberReversed = number.split("").reverse().join("")
    if (number === numberReversed)
        print("They are capicuas!")
};
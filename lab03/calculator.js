function display(value) {
    switch (value) {
        case "sqrt":
            document.getElementById("result").value = Math.sqrt(eval(document.getElementById("result").value));
            break;
        case "cbrt":
            document.getElementById("result").value = Math.cbrt(eval(document.getElementById("result").value));
            break;
        case "sin":
            document.getElementById("result").value = Math.sin(document.getElementById("result").value * Math.PI / 180);
            break;
        case "cos":
            document.getElementById("result").value = Math.cos(document.getElementById("result").value * Math.PI / 180);
            break;
        case "tan":
            document.getElementById("result").value = Math.tan(document.getElementById("result").value * Math.PI / 180);
            break;
        case "pow":
            document.getElementById("result").value = Math.eval(document.getElementById("result").value);
            break;
        default:
            document.getElementById("result").value += value;
    }
}

function result() {
    const inputElement = document.getElementById("result");
    const inputValue = inputElement.value;
    
    if (inputValue !== "") {
        const evaluatedValue = eval(inputValue);
        inputElement.value = evaluatedValue;
    }
}

function backspace() {
    var inputElement = document.getElementById("result");
    var inputValue = inputElement.value;
    
    inputElement.value = inputValue.slice(0, -1);
}

function cleardata() {
    var inputElement = document.getElementById("result");
    inputElement.value = "";
}

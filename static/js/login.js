console.log("PAGE IS BEING ACTIVATED");

function session_variables(){
    console.log("FUNCTION: session_variables()");

    localStorage.removeItem("email");
    localStorage.removeItem("password");

    const formData = new FormData(document.querySelector('form'))
    for (var pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
        localStorage.setItem(pair[0], pair[1]);
    }
}
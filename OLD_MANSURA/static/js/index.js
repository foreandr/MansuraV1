function radio_button_function(value) {
    console.log(value);

    if (value == "None") { document.getElementById("custom_source").innerHTML = `` }

    else if (value == "Mensura") {
        document.getElementById("custom_source").innerHTML = `

        `
    }
    else if (value == "Link") {
        document.getElementById("custom_source").innerHTML = `

        `
    }
}
function print_value() {
    console.log(document.getElementById("external_source").value)
}
/*
function get_size() {
    // console.log("hello world");
    var file = document.getElementById("dataset_file").files[0];
    //console.log(file);
    //console.log(file.size)
    if (file.size >= 10000) { // BYTES 10GB
        // console.log("FILE SIZE TOO BIG")
        document.getElementById("dataset_return_message").innerHTML = "FILE TOO BIG FOR NOW"
        // document.getElementById("dataset_file").value = null;
        document.getElementsByName("hidden_file_size").value = file.size
    } else {
        document.getElementById("hidden_file_size").value = file.size;
        document.getElementsByName("hidden_file_size").value = file.size
    }

}*/
function enable_built_from_other() {
    if (document.getElementById("external_source").disabled == true) {
        document.getElementById('external_source').removeAttribute("disabled");

    }
    else {
        document.getElementById("external_source").setAttribute("disabled", "enabled")
    }

}
function enable_exteral_link() {
    if (document.getElementById("external_source_link").disabled == true) {
        document.getElementById('external_source_link').removeAttribute("disabled");

    }
    else {
        document.getElementById("external_source_link").setAttribute("disabled", "enabled")
    }

}
/* When the user clicks on the button, toggle between hiding and showing the dropdown content
*/
function get_following() {
    console.log("FOLLOWERS: " + globalVariable.friends, "\nFOLLOWER AMOUNT",globalVariable.friends.length, "\NFOLLOWER ELSE:", globalVariable.friends[0])
    if (globalVariable.friends[0] != "NO FOLLOWING"){ // for some reason the global variable comes as an array not a string
        console.log("showing FOLLOWING");
        document.getElementById("my_following_dropdown").innerHTML = ""
        for (let i = 0; i < globalVariable.friends.length; i++){
            document.getElementById("my_following_dropdown").innerHTML += `<a href=/${globalVariable.friends[i]}>${globalVariable.friends[i]}</a>`
        }
        // document.getElementById("my_following_dropdown").innerHTML = `<a href=/${globalVariable.followers}>${globalVariable.friends}</a>`
        document.getElementById("my_following_dropdown").classList.toggle("show");
        
    }else{
        document.getElementById("my_following_dropdown").innerHTML = "NO FOLLOWIN"
        document.getElementById("my_following_dropdown").classList.toggle("show");
    }
    
}

/* When the user clicks on the button, toggle between hiding and showing the dropdown content
*/
function get_followers() {
    console.log("FOLLOWERS: " + globalVariable.followers, "\nFOLLOWER AMOUNT",globalVariable.followers.length, "\NFOLLOWER ELSE:", globalVariable.followers[0]);
    
    if (globalVariable.followers[0] != "NO FOLLOWERS"){
        //console.log("showing followers");
        document.getElementById("my_followers_dropdown").innerHTML = ""
        for (let i = 0; i < globalVariable.followers.length; i++){
            document.getElementById("my_followers_dropdown").innerHTML += `<a href=/${globalVariable.followers[i]}>${globalVariable.followers[i]}</a>`
        }
        //document.getElementById("my_followers_dropdown").innerHTML = `<a href=/${globalVariable.followers}>${globalVariable.friends}</a>`
        document.getElementById("my_followers_dropdown").classList.toggle("show");
    }else{
        document.getElementById("my_followers_dropdown").innerHTML = "NO followers"
        document.getElementById("my_followers_dropdown").classList.toggle("show");
    }
}


/* Close the dropdown menu if the user clicks outside of it
*/
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

/*
*/
function show_datasets(){
    //console.log("asljd");
    show_datasets()
}


function get_size(){
    // console.log("hello world");
    var file = document.getElementById("dataset_file").files[0];
    //console.log(file);
    //console.log(file.size)
    if (file.size >= 100000000){ // BYTES 10GB
        // console.log("FILE SIZE TOO BIG")
        document.getElementById("dataset_return_message").innerHTML = "FILE TOO BIG FOR NOW"
        document.getElementById("dataset_file").value = null;
    }else{
        document.getElementById("hidden_file_size").value = file.size;
    }
}


console.log("HELLO WORLD---------asddasasddsadsa---asddsadsa-------------------")



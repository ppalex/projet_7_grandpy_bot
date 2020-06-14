import {displayMap} from './google_map.js'


let form = document.querySelector("#form-question");
displayMap(-34.397, 150.644);

function send_data_to_backend(url, data) {

    return fetch(url, {
        method: "POST",
        body: data
    })
    .then()
    .catch(error => console.log(error));
}


function add_question_to_chat(question){
    let newDiv = document.createElement("div");
    let newP = document.createElement("p")
    let chatbox = document.querySelector("#chatbox");

    newDiv.setAttribute("class", "chatbox_question");

    newDiv.appendChild(newP);
    chatbox.appendChild(newDiv);
    console.log(question);
    newP.textContent = question;

}

function add_answer_to_chat(){
    
}


form.addEventListener('submit', function (event) {

    event.preventDefault();
    let question = document.querySelector('#question').value;
    add_question_to_chat(question);
    send_data_to_backend("/form", new FormData(form))

});



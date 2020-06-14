
let form = document.querySelector("#form-question");

function send_data_to_backend(url, data) {

    return fetch(url, {
        method: "POST",
        body: data
    })
    .then()
    .catch(error => console.log(error));
}


function add_question_to_chat(){
    let newDiv = document.createElement("div");
    let newP = document.createElement("p")
    let chat_box = document.querySelector("#chatbox");

    newDiv.setAttribute("class", "chatbox_question");

    newDiv.appendChild(newP);
    chat_box.appendChild(newDiv);
    
    newP.textContent = question;

}

function add_answer_to_chat(){
    
}


form.addEventListener('submit', function (event) {

    event.preventDefault();
    question = document.querySelector('#question').value;
    console.log(question);
    add_question_to_chat(question);
    send_data_to_backend("/form", new FormData(form))

});



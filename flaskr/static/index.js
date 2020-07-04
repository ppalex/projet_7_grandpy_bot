import { displayMap } from './google_map.js'


let form = document.querySelector("#form-question");

function send_data_to_backend(url, data) {

    return fetch(url, {
        method: "POST",
        body: data
    })
        .then(response => response.json())
        .catch(error => console.log(error));
}

function add_question_to_chat(question) {
    let newDiv = document.createElement("div");
    let newP = document.createElement("p");
    let newIm = document.createElement("img");
    let time = document.createElement("span");

    let chatbox = document.querySelector("#chatbox");

    newDiv.setAttribute("class", "chatbox_question");
    newIm.setAttribute("src", "../static/images/user.png");
    newIm.setAttribute("style", "width:100%");
    time.setAttribute("class", "time-right");

    newDiv.appendChild(newIm);
    newDiv.appendChild(newP);
    newDiv.appendChild(time);
    chatbox.appendChild(newDiv);

    newP.textContent = question;
    time.textContent = get_current_time();

}

function add_answer_to_chat(answer, wiki_url) {

    let newDiv = document.createElement("div");
    let newP = document.createElement("p");
    let chatbox = document.querySelector("#chatbox");
    let newIm = document.createElement("img");
    let time = document.createElement("span");

    newDiv.setAttribute("class", "chatbox_answer");
    newIm.setAttribute("src", "../static/images/grandpy.png");
    newIm.setAttribute("style", "width:100%");
    time.setAttribute("class", "time-left");

    newDiv.appendChild(newIm);
    newDiv.appendChild(newP);
    newDiv.appendChild(time);
    chatbox.appendChild(newDiv);

    newP.textContent = answer;
    time.textContent = get_current_time();

    if (wiki_url != null) {
        let link_p = document.createElement("p");
        let wiki_link = document.createElement("a");
        let bracket_opened = document.createTextNode('[');
        let bracket_closed = document.createTextNode(']');


        wiki_link.setAttribute("href", wiki_url);
        newP.appendChild(link_p);
        wiki_link.textContent = "En savoir plus sur Wikipedia";
        link_p.appendChild(bracket_opened);
        link_p.appendChild(wiki_link);
        link_p.appendChild(bracket_closed);
    }
}

function get_current_time() {

    let today = new Date();

    let hour = today.getHours();
    let minute = today.getMinutes();

    if (hour < 10) {
        hour = "0" + hour;
    }

    if (minute < 10) {
        minute = "0" + minute;
    }

    let time = hour + ":" + minute;

    return time;
}


form.addEventListener('submit', function (event) {

    event.preventDefault();
    let question = document.querySelector('#question').value;

    if ((/[A-Za-z,;'"\séà-ç]+\?/g).test(question) !== true) {
        alert("Les données ne sont pas valides.");
    }

    else {

        add_question_to_chat(question);
        document.getElementById('loader').style.display = 'block';
        send_data_to_backend("/form", new FormData(form))
            .then(response => {
                
                let status = response["status"];

                if (status == "OK") {
                    let lat = response["latitude"];
                    let lng = response["longitude"];
                    let url = response["url"];
                    let message_for_address = response["message_for_address"];
                    let message_for_story = response["message_for_story"]
                    console.log(response);
                    add_answer_to_chat(message_for_address, null);
                    add_answer_to_chat(message_for_story, url);
                    displayMap(lat, lng);
                    
                }
                else {
                    let message_for_error = response["message_for_error"];
                    add_answer_to_chat(message_for_error, null);
                }
                document.getElementById('loader').style.display = 'None';            

            });
            
    }
});



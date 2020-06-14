function displayMap(latitude, longitude){

    let map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: latitude, lng: longitude },
        zoom: 8
      });

}

export {displayMap};
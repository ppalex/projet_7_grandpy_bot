function displayMap(latitude, longitude){

    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: latitude, lng: longitude },
        zoom: 8
      });

}

displayMap(-34.397, 150.644);
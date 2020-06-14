function displayMap(latitude, longitude){

    let map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: latitude, lng: longitude },
        zoom: 15
      });

      let marker = new google.maps.Marker({
        position: {lat: latitude, lng: longitude },
        map: map
      });

}

export {displayMap};
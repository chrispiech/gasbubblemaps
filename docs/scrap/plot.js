// This example creates a 2-pixel-wide red polyline showing the path of
// the first trans-Pacific flight between Oakland, CA, and Brisbane,
// Australia which was made by Charles Kingsford Smith.

var map = null



function plotPaths(pathData){
  for (var i = 0; i < pathData.length; i++) {
    let currPath = pathData[i]
    plotPath(currPath)
  }
}

function plotPoints(pointsData) {
  for (var i = 0; i < pointsData.length; i++) {
    let currPoint = pointsData[i]
    plotPoint(currPoint)
  }
}

function loadJSON(fileName, callback) {   

    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
    xobj.open('GET', fileName, true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    xobj.send(null);  
 } 

 function plotPath(rawPath){
  const cleanPathPoints = []
  for(var i = 0; i < rawPath.length; i++) {
    let rawPoint = rawPath[i]
    let cleanPoint = {
      lat: rawPoint[1],
      lng: rawPoint[0]
    }
    cleanPathPoints.push(cleanPoint)
  }

  const cleanPath = new google.maps.Polyline({
    path: cleanPathPoints,
    geodesic: true,
    strokeColor: "#0000FF",
    strokeOpacity: 0.8,
    strokeWeight: 1.5
  });
  cleanPath.setMap(map);
}

function plotPoint(rawPoint){

  const point = new google.maps.Marker({
    map: map,
    position: {
      lat:rawPoint[1],
      lng:rawPoint[0]
    },
    icon: {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: '#F00',
        fillOpacity: 0.6,
        strokeColor: '#A00',
        strokeOpacity: 0.9,
        strokeWeight: 1,
        scale: 3
    }
  });
  point.setMap(map);
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10,
    center: { lat: 37.449925, lng: -122.161760 },
    mapTypeId: "roadmap"
  });
  loadJSON('paths.json', function(response) {
  // Parse JSON string into object
    var pathData = JSON.parse(response);
    plotPaths(pathData)
  })
  loadJSON('stopPoints.json', function(response) {
  // Parse JSON string into object
    var pointsData = JSON.parse(response);
    plotPoints(pointsData)
  })
  
}
// This example creates a 2-pixel-wide red polyline showing the path of
// the first trans-Pacific flight between Oakland, CA, and Brisbane,
// Australia which was made by Charles Kingsford Smith.

const FEET_TO_METERS = 0.3048

var map = null
var nearBayJson = null
var markersArray = []

function maxHeightChange(newValue) {
  console.log(newValue)
  $("#heightLabelValue").html(newValue)
  clearOverlays()
  plotHeight(newValue)
}

function clearOverlays() {
  for (var i = 0; i < markersArray.length; i++ ) {
    markersArray[i].setMap(null);
  }
  markersArray = []
}



function plotHeight(maxElevationFeet) {
  let maxElevationMeters = maxElevationFeet * FEET_TO_METERS
  for(var index in nearBayJson) {
    let path = nearBayJson[index]
    console.log(path)
      plotPath(path, maxElevationMeters)
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

 function plotPoints(pointsData) {
  for (var i = 0; i < pointsData.length; i++) {
    let currPoint = pointsData[i]
    // console.log(currPoint)
    plotPoint(currPoint)
    // if(i == 300) { break}
  }
}

 function plotPath(rawPath, maxElevation){
  const cleanPathPoints = []
  // special case a path that starts too high
  // if(rawPath[0][2] >= maxElevation) {
  //   return
  // }
  for(var i = 0; i < rawPath.length; i++) {
    let rawPoint = rawPath[i]
    let elevation = 500//rawPoint[2]
    // if(elevation >= maxElevation) {
    //   plotPoint(rawPoint)
    //   break
    // }
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
  markersArray.push(cleanPath)
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
  markersArray.push(point)
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 9,
    center: { lat: 37.449925, lng: -122.161760 },
    mapTypeId: "roadmap"
  });
  loadJSON('ca_roads.json', function(response) {
    nearBayJson = JSON.parse(response);
    plotHeight(1000)
  })
  loadJSON('intersections.json', function(response) {
  // Parse JSON string into object
    let intersections = JSON.parse(response);
    plotPoints(intersections)
  })
  
}
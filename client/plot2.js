// This example creates a 2-pixel-wide red polyline showing the path of
// the first trans-Pacific flight between Oakland, CA, and Brisbane,
// Australia which was made by Charles Kingsford Smith.

const FEET_TO_METERS = 0.3048
const INIT_HEIGHT = 1000
var map = null
var data = {}
var markersArray = []

function maxHeightChange(newValue) {
  clearOverlays()
  plotHeight(newValue)
}

function clearOverlays() {
  for (var i = 0; i < markersArray.length; i++ ) {
    markersArray[i].setMap(null);
  }
  markersArray = []
}

function plotPoints(pointsData) {
  for (var i = 0; i < pointsData.length; i++) {
    let currPoint = pointsData[i]
    // console.log(currPoint)
    plotPoint(currPoint)
    // if(i == 300) { break}
  }
}

function plotHeight(maxElevationFeet) {
  let fileName = 'data/dfs' + maxElevationFeet + '.json'
  let heightData = data[fileName]
  $("#heightLabelValue").html(maxElevationFeet)
  $("#heightInput").val(maxElevationFeet)
  let maxElevationMeters = maxElevationFeet * FEET_TO_METERS
  for(var key in heightData) {
    let path = heightData[key]
    if(path != null){
      plotPath(path, maxElevationMeters)
    }
  }
}

function loadJSON(fileName, callback) {   

    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
    xobj.open('GET', fileName, true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText, fileName);
          }
    };
    xobj.send(null);  
 } 

 function plotPath(rawPath, maxElevation){
  const cleanPathPoints = []
  // special case a path that starts too high
  if(rawPath[0][2] >= maxElevation) {
    return
  }
  for(var i = 0; i < rawPath.length; i++) {
    let rawPoint = rawPath[i]
    let elevation = rawPoint[2]
    if(elevation >= maxElevation) {
      plotPoint(rawPoint)
      break
    }
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
    strokeOpacity: 1,
    strokeWeight: 1.2
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
        fillOpacity: 0.8,
        strokeColor: '#A00',
        strokeOpacity: 1,
        strokeWeight: 1,
        scale: 4
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
  // first load the 1k data
  loadJSON('data/dfs' +INIT_HEIGHT +'.json', function(response, fileName) {
      data[fileName] = JSON.parse(response);
      let nLoaded = Object.keys(data).length
      plotHeight(INIT_HEIGHT)
      if(nLoaded == 26) {
        console.log('ready')
        $( "#heightInput" ).prop( "disabled", false );
      }
    })

  for (var i = 500; i <= 3000; i+= 100) {
    if(i == INIT_HEIGHT) continue
    let file = 'data/dfs' + i + '.json'
    loadJSON(file, function(response, fileName) {
      data[fileName] = JSON.parse(response);
      let nLoaded = Object.keys(data).length
      console.log(fileName, nLoaded)
      if(nLoaded == 26) {
        console.log('ready')
        $( "#heightInput" ).prop( "disabled", false );
      }
    })
  }
  
}
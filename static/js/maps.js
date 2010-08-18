<!--
  var geocoder;
  var map;
  var mgr;
  var pb;
  var num = 0;
  var actives = 0; //number of currently available trucks
  var chicago = new google.maps.LatLng(41.850033, -87.6500523);
  var test_latlng =	 [
	new google.maps.LatLng( 34.05349, -118.245319 ),
	new google.maps.LatLng( 34.07222, -118.245319 ),
	new google.maps.LatLng( 34.05345, -118.247322 ),
	new google.maps.LatLng( 34.07340, -118.254319 ),
	new google.maps.LatLng( 34.02339, -118.306319 ),
	new google.maps.LatLng( 34.05949, -118.275119 ),
	new google.maps.LatLng( 34.04149, -118.215319 )
  ];
  
  function initialize() {
	geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng( 34.05349, -118.245319 )
    var myOptions = {
      zoom: 12,
      center: latlng,
	  mapTypeControl: false,
	  navigationControl: true,
	  scaleControl: false,
	  scrollwheel: false,
	  mapTypeControlOptions: {
	    style: google.maps.MapTypeControlStyle.DEFAULT,
		position: google.maps.ControlPosition.BOTTOM
		},
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	mgr = new MarkerManager(map);
	pb = new progressBar();
	map.controls[google.maps.ControlPosition.TOP_RIGHT].push(pb.getDiv());

	google.maps.event.addListener(mgr, 'loaded', function()	{
		populate();
	});
/**
	// create the DIV to hold the control and call the populateTrucks() constructor
	// passing in this DIV
	var populateTrucksDIV = document.createElement('DIV');
	var removeTrucksDIV = document.createElement('DIV');
	var truckpop = new populateTrucks(populateTrucksDIV, map);
	var truckremove = new removeTrucks(removeTrucksDIV, map);
	
	populateTrucksDIV.index = 1;
	removeTrucksDIV.index = 2;
	map.controls[google.maps.ControlPosition.TOP_LEFT].push(populateTrucksDIV);	
	map.controls[google.maps.ControlPosition.TOP_RIGHT].push(removeTrucksDIV);	
**/
  }  
 
  function codeAddress() {
    var center;
	var address = document.getElementById("address").value;
    if (geocoder) {
      geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          center = results[0].geometry.location;
		  map.setCenter(center);
		  clear();
		  populate();
        } else {
          alert("Geocode was not successful for the following reason: " + status);
        }
      });
    }
  }
 
  function populate()	{
	var title, posn, marker;
    actives = test_latlng.length;
	pb.start(actives);
	// Dummy markers
	marker = createMarker(test_latlng[num], 'LA', false);
	mgr.addMarker(marker, 5);
	//mgr.refresh();
	num++; 	
	pb.updateBar(num);
	if(num < actives)	{
		setTimeout(populate, 200);
	} else	{
		pb.hide();
	}
  }

  function add_marker(point) {
	var pnt = point.properties;
	var lat = point.geometry.coordinates[1];
	var lon = point.geometry.coordinates[0];
}  
  
  function createMarker(posn, title, icon)	{
	var markerOptions =	{
		position: posn,
		title: title
	};
	if(icon !== false)	{
		markerOptions.shadow = icon.shadow,
		markerOptions.icon = icon.icon,
		markerOptions.shape = icon.shape
	};
	var marker = new google.maps.Marker(markerOptions);
	return marker;
  }
  
  function clear()  {
	pb.updateBar(-num);
	num = 0;
	pb.hide();
	mgr.clearMarkers();
  }

/**
  // populateTrucks adds a control to the map that populates markers 
  // on the map with nearby food trucks. This constructor takes the 
  // control DIV as an argument.
  function populateTrucks(controlDiv, map)  {
    // Set CSS styles for the DIV containing the control
    controlDiv.style.padding = '15px';
  
    // Set CSS for the control border
    var controlUI = document.createElement('DIV');
    controlUI.style.backgroundColor = 'black';
    controlUI.style.borderStyle = 'solid';
    controlUI.style.borderWidth = '2px';
    controlUI.style.cursor = 'pointer';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Dynamically populates food trucks';
    controlDiv.appendChild(controlUI);
	
	// Set CSS for the control interior
	var controlText = document.createElement('DIV');
    controlText.style.fontFamily = 'Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.paddingLeft = '4px';
    controlText.style.paddingRight = '4px';
    controlText.innerHTML = '<b>Populate Trucks</b>';
    controlUI.appendChild(controlText);
	
    google.maps.event.addDomListener(controlUI, 'click', function()	{
		loadMarkers();
	});
	
	// Setup the click event listeners: simply set the map to
    // Chicago
    //google.maps.event.addDomListener(controlUI, 'click', function() {
      //map.setCenter(chicago)
    //});
}

  function removeTrucks(controlDiv, map)  {
    // Set CSS styles for the DIV containing the control
    controlDiv.style.padding = '15px';
  
    // Set CSS for the control border
    var controlUI = document.createElement('DIV');
    controlUI.style.backgroundColor = 'black';
    controlUI.style.borderStyle = 'solid';
    controlUI.style.borderWidth = '2px';
    controlUI.style.cursor = 'pointer';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Removes food truck markers';
    controlDiv.appendChild(controlUI);
	
	// Set CSS for the control interior
	var controlText = document.createElement('DIV');
    controlText.style.fontFamily = 'Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.paddingLeft = '4px';
    controlText.style.paddingRight = '4px';
    controlText.innerHTML = '<b>Remove Trucks</b>';
    controlUI.appendChild(controlText);
	
    // Setup the click event listeners: simply set the map to
    // Chicago
    google.maps.event.addDomListener(controlUI, 'click', function() {
	  loadMarkers();
	});
  }
 **/ 
  
//-->
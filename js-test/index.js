d3.select('body').append('svg').attr('class','bar-chart')

var dataset = [90,30,80,200];
var svgWidth = 500, barpadding = 5, topPadding = 20;
var svgHeight = Math.max(...dataset) + topPadding;
var barWidth = (svgWidth/dataset.length);

var svg = d3.select('svg')
    .attr('width',svgWidth)
    .attr('height',svgHeight);

var barChart = svg.selectAll('rect')
    .data(dataset)
    .enter()
    .append('rect')
    .attr('y', function(d) { return svgHeight - d})
    .attr('height', function(d) {return d;})
    .attr('width', barWidth - barpadding)
    .attr('transform', function(d,i) {
        var translate = [barWidth*i,0];
        return "translate(" + translate + ")";
    });



// create Leaflet map
var map = L.map('map', {
  minZoom: 0,
  maxZoom: 6
});

var rc = new L.RasterCoords(map, [3185, 4763]);
rc.setMaxBounds();
var mapBounds = rc.getMaxBounds();
// set the map to fit the world
map.fitBounds(mapBounds);

// the tile layer containing the image generated with gdal2tiles --leaflet ...
L.tileLayer('https://loremaps.github.io/LoreMaps-Faerun-Tiles/Tiles/{z}/{x}/{y}.png', {
  noWrap: true,
  bounds: mapBounds
}).addTo(map);



// add the attributions
var attributionControl = map.attributionControl;
attributionControl.addAttribution('<a href="https://loremaps.azurewebsites.net/">LoreMaps</a>');
attributionControl.addAttribution('Map data <a href="http://www.pocketplane.net/">Pocket Plane Group</a>');

// create the market
var tooltip = L.tooltip().setLatLng(rc.unproject([409, 313])).setContent('Test Tooltip').addTo(map);
//var circle = L.circle(rc.unproject([409, 313]), {radius: 5}).addTo(map);

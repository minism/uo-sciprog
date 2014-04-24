// Geographical plot of event data using d3.js geo projection.
// See: http://bl.ocks.org/mbostock/3757132


// Export init function
window.initSolution = function(events) {
  createProjection(function(projection) {
    plotEvents(projection, events);
  });
};


/* Plot event data */
var plotEvents = function(projection, events) {
  var circle = d3.select('svg').selectAll('.event').data(events).enter()
    .append('circle').attr('class', 'event');
  styleCircle(circle);

  // Project onto map
  circle.attr('transform', function(ev) {
    return 'translate(' + projection([ev.lon, ev.lat]) + ')'
  });
};


/* Style an individual event circle */
var styleCircle = function(circle) {
  return circle.attr('r', 5);
}


/* Initialize the mercator projection and invoke callback with it */
var createProjection = function(callback) {
  // Create SVG element
  var width = 800, height = 600;
  var svg = d3.select("#wrap").append("svg")
      .attr("width", width)
      .attr("height", height);

  var projection = d3.geo.mercator()
      .scale((width + 1) / 2 / Math.PI)
      .translate([width / 2, height / 2])
      .precision(.1);

  var path = d3.geo.path().projection(projection);

  d3.json("/static/data/world-50m.json", function(error, world) {
    // Insert land vectors
    svg.insert("path", ".graticule")
        .datum(topojson.feature(world, world.objects.land))
        .attr("class", "land")
        .attr("d", path);

    // Insert country borders
    svg.insert("path", ".graticule")
        .datum(topojson.mesh(
            world, world.objects.countries, function(a, b) { return a !== b; }))
        .attr("class", "boundary")
        .attr("d", path);

    // Invoke callback
    callback(projection);
  });

  // d3.select(self.frameElement).style("height", height + "px");
};
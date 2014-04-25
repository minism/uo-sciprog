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
      .append('circle')
      .attr('class', 'event')
      .attr('r', function(ev) {
        // Use magnitude cubed for radius to visualize variance better
        return ev.m * ev.m * ev.m / 90;
      });

  // Project onto map
  circle.attr('transform', function(ev) {
    return 'translate(' + projection([ev.lon, ev.lat]) + ')'
  });
};


/* Initialize the mercator projection and invoke callback with it */
var createProjection = function(callback) {
  // Create SVG element
  var width = 1024, height = 768;
  var svg = d3.select("body").append("svg")
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
};
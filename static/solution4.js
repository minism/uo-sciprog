// Timeline plot of event data using d3.js
var WIDTH = 800;
var HEIGHT = 600;
var STARTYEAR = 1900;
var ENDYEAR = 2008;


// Export init function
window.initSolution = function(events) {
  plotEvents(events);
};


/* Create the chart layout and plot events */
var plotEvents = function(events) {
  // Create SVG element
  var svg = d3.select("#wrap").append("svg")
      .attr("width", WIDTH)
      .attr("height", HEIGHT);

  svg.selectAll('.event').data(events).enter()
      .append('circle')
      .attr('class', 'event')
      .attr('cx', transform_x)
      .attr('cy', transform_y)
      .attr('r', function(ev) {
        return ev.m;
      });
}


/* Coordinate transformation functions for charts */
var transform_x = function(ev) {
  var pos = (ev.y - STARTYEAR) / (ENDYEAR - STARTYEAR);
  return pos * WIDTH;
}
var transform_y = function(ev) {
  var pos = (ev.lat + 90) / 180;
  return HEIGHT - pos * HEIGHT;
}

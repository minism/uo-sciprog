// Timeline plot of event data using d3.js
var WIDTH = 800;
var HEIGHT = 600;


// Export init function
window.initSolution = function(events) {
  // Merge year data
  var yearData = mergeYearData(events);
  plotYearData(yearData);
};


/* Create the chart layout and plot year data */
var plotYearData = function(yearData) {
  // Create SVG element
  var svg = d3.select("#wrap").append("svg")
      .attr("width", WIDTH)
      .attr("height", HEIGHT);

  var padding = 50;
  var width = WIDTH - padding;
  var height = HEIGHT - padding;

  // Create axes
  var years = _.pluck(yearData, 'year')
  var x = d3.scale.linear()
      .domain([_.min(years), _.max(years)])
      .range([padding, width]);

  var magnitudes = _.pluck(yearData, 'magnitude')
  var y = d3.scale.linear()
      .domain([_.min(magnitudes), _.max(magnitudes)])
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(10);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + (height + 5) + ")")
      .call(xAxis)
    .append("text")

  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + padding +  ",0)")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Average magnitude")

  // Plot events
  svg.selectAll('.bar').data(yearData).enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', function(ev) { return x(ev.year) })
      .attr('width', 5)
      .attr('y', function(ev) { return y(ev.magnitude) })
      .attr('height', function(ev) { return height - y(ev.magnitude) });
};


/* Calculate mean magnitudes for all years */
var mergeYearData = function (events) {
  console.log(events);
  var years = {};
  _.map(events, function(ev) {
    years[ev.y] = years[ev.y] === undefined ? [] : years[ev.y]
    years[ev.y].push(parseFloat(ev.m))
  });
  _.map(years, function(magnitudes, year) {
    var sum = _.reduce(magnitudes, function(a, b) { return a + b; }, 0);
    years[year] = sum / magnitudes.length;
  });

  return _.map(years, function(magnitude, year) {
    return {
      magnitude: magnitude,
      year: parseInt(year)
    }
  });
};
// Timeline plot of event data using d3.js
var WIDTH = 1024;
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
  var svg = d3.select("body").append("svg")
      .attr("width", WIDTH)
      .attr("height", HEIGHT);

  var padding = 50;
  var width = WIDTH - padding;
  var height = HEIGHT - padding;

  // Create axes
  var years = _.pluck(yearData, 'year')
  var minYear = _.min(years), maxYear = _.max(years);
  var x = d3.scale.linear()
      .domain([minYear, maxYear + 1])
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
      .text("Year")
      .attr("transform", "translate(" + width / 2 + ", 40)");

  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + padding +  ",0)")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Total magnitude")

  // Setup tooltip
  var popup = d3.tip()
      .attr('class', 'popup')
      .offset([-10, 0])
      .html(function(d) {
        return d.year + " - " + d.count + " earthquakes with " + 
               d.magnitude.toFixed(1) + " total magnitude";
      })
  svg.call(popup);

  // Compute bar width
  var width = WIDTH / (maxYear - minYear + 10) - 1;

  // Plot events
  svg.selectAll('.bar').data(yearData).enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', function(ev) { return x(ev.year) })
      .attr('width', width)
      .attr('y', function(ev) { return y(ev.magnitude) })
      .attr('height', function(ev) { return height - y(ev.magnitude) })
      .on('mouseover', popup.show)
      .on('mouseout', popup.hide);
};


/* Calculate properties for all years */
var mergeYearData = function (events) {
  var years = {};

  // Group events by year
  _.map(events, function(ev) {
    years[ev.y] = years[ev.y] === undefined ? [] : years[ev.y]
    years[ev.y].push(parseFloat(ev.m))
  });

  // Determine sum magnitude for each year
  _.map(years, function(magnitudes, year) {
    var sum = _.reduce(magnitudes, function(a, b) { return a + b; }, 0);
    years[year] = [sum, magnitudes.length];
  });

  return _.map(years, function(val, year) {
    return {
      magnitude: val[0],
      count: val[1],
      year: parseInt(year)
    }
  });
};
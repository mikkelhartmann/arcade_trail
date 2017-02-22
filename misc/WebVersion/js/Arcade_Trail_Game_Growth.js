(function(){
    /**
     * Select the SVG tag from the DOM so we can add new children to it
     */
    var svg = d3.select('#Arcade_Trail_Game_Growth');

    /**
     * Various constant variables that we have here for convenience.
     */
    var margin = {
        left: 30,
        top: 30,
        right: 30,
        bottom: 30,
    };

    var outerWidth = parseInt(svg.attr('width'));
    var outerHeight = parseInt(svg.attr('height'));
    var innerWidth = outerWidth - margin.left - margin.right;
    var innerHeight = outerHeight - margin.top - margin.bottom;

    // The name of the columns from the CSV file that should be used
    // for the x and y coordinates respectively and the series.
    var xColumn = 'x';
    var yColumn = 'y';
    var seriesColumn = 's';

    /**
     * Create the `g` SVG elements  that we're going to use for our rendering of the
     * data and the x and y axis.
     */
    var g = svg.append('g')
        .attr('transform', 'translate('+ margin.left +', '+ margin.top +')');

    // NOTE: We use translate to move the x-axsis to the bottom of the chart.
    var xAxisG = g.append('g')
        .attr('transform', 'translate(0, ' + innerHeight + ')')
        .attr('class', 'axis');

    var yAxisG = g.append('g')
        .attr('class', 'axis');

    /**
     * Define our scales.
     */
    var xScale = d3.scale.linear().range([0, innerWidth]);

    // NOTE: (0,0) in the SVG coordinate system is the upper left corner of the SVG
    // element. Thus we have to inverse the max/min of the y axises to get (0,0) to
    // be in the lower left corner as expected.
    var yScale = d3.scale.linear().range([innerHeight, 0]);

    // Here we define which colors our series should be mapped to.
    var seriesScale = d3.scale.ordinal()
        .range(['#1f77b4', '#ff7f0e', '#2ca02c']);

    /**
     * Set up our axises using d3.svg.axis and our scales.
     */
    var xAxis = d3.svg.axis().scale(xScale).orient('bottom');
    var yAxis = d3.svg.axis().scale(yScale).orient('left');

    /**
     * Describe how we want to visualize our data.
     */
    function render(data) {
        // Set the domain of the scales (input ranges). d3.extend returns an array
        // with two elements representing the max and min of the given column.
        xScale.domain(d3.extent(data, function(d) { return d[xColumn]; }));
        yScale.domain(d3.extent(data, function(d) { return d[yColumn]; }));
        seriesScale.domain(data.map(function(d) { d[seriesColumn]; }));

        // Render our x and y axis
        xAxisG.call(xAxis);
        yAxisG.call(yAxis);

        // Bind the data
        var circles = g.selectAll('circle').data(data);

        // Create circle svg elements for each data entry
        circles.enter().append('circle')
            .attr('r', 5)
            .attr('class', 'dot');

        // Update
        // Here we use our scales to map our x and y values to pixels
        // and our series to a color.
        circles
            .attr('cx', function(d) { return xScale(d[xColumn]); })
            .attr('cy', function(d) { return yScale(d[yColumn]); })
            .attr('fill', function(d) { return seriesScale(d[seriesColumn]); });

        // Exit
        circles.exit().remove();
    }

    /* Parse the data and invoke our render funciton */
    function parse(d) {
        d[xColumn] = parseFloat(d[xColumn]);
        d[yColumn] = parseFloat(d[yColumn]);
        return d;
    }

    d3.csv('scatter-plot.csv', parse, render);
})();

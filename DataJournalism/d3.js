//==================================
// Set up our chart
//==================================
var svgWidth = 600
var svgHeight = 400;

var margin = { top: 20, right: 40, bottom: 100, left: 120 };
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;


// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3
	.select(".chart")
	.append("svg")
	//responsive SVG needs these 2 attributes and no width and height attr
	.attr("preserveAspectRatio", "xMinYMin meet")
	.attr("viewBox", "0 0 600 400")
	//class to make it responsive
	.classed("svg-content-responsive", true)
	// remove SVG width and height and use responsive attributes instead
	// .attr("width", svgWidth)
	// .attr("height", svgHeight)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Append an SVG group
var chart = svg.append("g");

// Append a div to the bodyj to create tooltips, assign it a class
d3.select(".chart").append("div").attr("class", "tooltip").style("opacity", 0);

// Retrieve data from the CSV file and execute everything below
d3.csv("data.csv", function(err, stateData) {
	if (err) throw err;

	stateData.forEach(function(data) {
		data.id = +data.id;
		data.depression = +data.depression;
		data.smokes = +data.smokes;
		data.obese = +data.obese;
		data.unemployment = +data.unemployment;
		data.poverty = +data.poverty;
		data.uninsured = +data.uninsured;
	});

	// Create scale functions
	var yLinearScale = d3.scaleLinear().range([height, 0]);
	var xLinearScale = d3.scaleLinear().range([0, width]);

	// Create axis functions
	var bottomAxis = d3.axisBottom(xLinearScale);
	var leftAxis = d3.axisLeft(yLinearScale);

	// These variables store the minimum and maximum values in a column in data.csv
	var xMin;
	var xMax;
	var yMax;

	// This function identifies the minimum and maximum values in a column in data.csv
	// and assign them to xMin and xMax variables, which will define the axis domain
	function findMinAndMax(dataColumnX, dataColumnY) {
		xMin = d3.min(stateData, function(data) {
		return +data[dataColumnX] * 0.8;
		});

		xMax = d3.max(stateData, function(data) {
		return +data[dataColumnX] * 1.1;
		});

		yMax = d3.max(stateData, function(data) {
		return +data[dataColumnY] * 1.1;
		});
	}

	// The default x-axis is 'poverty', y-axis is 'depression'
	// Another axis can be assigned to the variable during an onclick event.
	// This variable is key to the ability to change axis/data column
	var currentAxisLabelX = "poverty";
	var currentAxisLabelY = "depression"

	// Call findMinAndMax() with 'poverty' as default
	findMinAndMax(currentAxisLabelX, currentAxisLabelY);

	// Set the domain of an axis to extend from the min to the max value of the data column
	xLinearScale.domain([xMin, xMax]);
	yLinearScale.domain([0, yMax]);

		// Initialize tooltip
	var toolTip = d3
		.tip()
		.attr("class", "tooltip")
		// Define position
		.offset([80, -60])
		// The html() method allows us to mix JavaScript with HTML in the callback function
		.html(function(data) {
		var stateName = data.state;
		var depression = +data.depression;
		var smokes = +data.smokes;
		var obese = +data.obese;
		var unemployment = +data.unemployment;
		var poverty = +data.poverty;
		var uninsured = +data.uninsured;

		var xString;
		if (currentAxisLabelX === "poverty") {
			xString = "<br> In Poverty (%): " + poverty;
		} else if (currentAxisLabelX === "uninsured") {
			xString ="<br> Uninsured (%): " + uninsured;
		}  else {
			xString ="<br> Unemployment (%): " + unemployment;
		}

		var yString;
		if (currentAxisLabelY === "depression") {
			yString = "<br> Depression (%): " + depression;
		} else if (currentAxisLabelY === "smokes") {
			yString ="<br> Smokes (%): " + smokes;
		}  else {
			yString ="<br> Obese (%): " + obese;
		}

		return stateName + xString + yString;
	});

	// Create tooltip
	chart.call(toolTip);
	chart
		.selectAll("circle")
		.data(stateData)
		.enter()
		.append("circle")
		.attr("cx", function(data, index) {
		return xLinearScale(+data[currentAxisLabelX]);
		})
		.attr("cy", function(data, index) {
		return yLinearScale(+data[currentAxisLabelY]);
		})
		.attr("r", "15")
		.attr("fill", "#E75480")
		.attr('fill-opacity', 0.35)
		// display tooltip on click
		.on("mouseover", function(data) {
		toolTip.show(data);
		})
		// hide tooltip on mouseout
		.on("mouseout", function(data, index) {
		toolTip.hide(data);
		});

	// create circle text
	var text = chart
		.selectAll("text")
		.data(stateData)
		.enter()
		.append("text")
	var textLabels = text
		.attr("x", function(data, index) {
			return xLinearScale(+data[currentAxisLabelX])-6;
		})
		.attr("y", function(data, index) {
			return yLinearScale(+data[currentAxisLabelY])+4;
		})
		.text( function (data) {return data.abbr})
		.attr("class","circle-text");

	// Append an SVG group for the x-axis, then display the x-axis
	chart
		.append("g")
		.attr("transform", "translate(0," + height + ")")
		// The class name assigned here will be used for transition effects
		.attr("class", "x-axis")
		.call(bottomAxis);

	// Append a group for y-axis, then display it
	chart.append("g").call(leftAxis);

	// Append multiple y-axis label
	chart
		.append("text")
		.attr("transform", "rotate(-90)")
		.attr("y", 0 - margin.left + 60)
		.attr("x", 0 - height / 2)
		.attr("dy", "1em")
		.attr("class", "yaxis-text yactive")
		.attr("data-axis-name", "depression")
		.text("Depression (%)");

	chart
		.append("text")
		.attr("transform", "rotate(-90)")
		.attr("y", 0 - margin.left + 40)
		.attr("x", 0 - height / 2)
		.attr("dy", "1em")
		.attr("class", "yaxis-text yinactive")
		.attr("data-axis-name", "smokes")
		.text("Smokes (%)");

	chart
		.append("text")
		.attr("transform", "rotate(-90)")
		.attr("y", 0 - margin.left + 20)
		.attr("x", 0 - height / 2)
		.attr("dy", "1em")
		.attr("class", "yaxis-text yinactive")
		.attr("data-axis-name", "obese")
		.text("Obese (%)");

	// Append multiple x-axis labels
	chart
		.append("text")
		.attr(
		"transform",
		"translate(" + width / 2 + " ," + (height + margin.top + 20) + ")"
		)
		.attr("class", "xaxis-text xactive")
		.attr("data-axis-name", "poverty")
		.text("In Poverty (%)");

	chart
		.append("text")
		.attr(
			"transform",
			"translate(" + width / 2 + " ," + (height + margin.top + 40) + ")"
		)
		.attr("class", "xaxis-text xinactive")
		.attr("data-axis-name", "unemployment")
		.text("Unemployment (%)");

	chart
		.append("text")
		.attr(
			"transform",
			"translate(" + width / 2 + " ," + (height + margin.top + 60) + ")"
		)
		.attr("class", "xaxis-text xinactive")
		.attr("data-axis-name", "uninsured")
		.text("Uninsured (%)");

	// Change an axis's status from inactive to active when clicked (if it was inactive)
	// Change the status of all active axes to inactive otherwise
	function xlabelChange(clickedAxis) {
		d3
		.selectAll(".xaxis-text")
		.filter(".xactive")
		// An alternative to .attr("class", <className>) method. Used to toggle classes.
		.classed("xactive", false)
		.classed("xinactive", true);

		clickedAxis.classed("xinactive", false).classed("xactive", true);
	}

	function ylabelChange(clickedAxis) {
		d3
		.selectAll(".yaxis-text")
		.filter(".yactive")
		// An alternative to .attr("class", <className>) method. Used to toggle classes.
		.classed("yactive", false)
		.classed("yinactive", true);

		clickedAxis.classed("yinactive", false).classed("yactive", true);
	}

	d3.selectAll(".xaxis-text").on("click", function() {
		// Assign a variable to current axis
		var clickedSelection = d3.select(this);
		// "true" or "false" based on whether the axis is currently selected
		var isClickedSelectionInactive = clickedSelection.classed("xinactive");
		// console.log("this axis is inactive", isClickedSelectionInactive)
		// Grab the data-attribute of the axis and assign it to a variable
		// e.g. if data-axis-name is "poverty," var clickedAxis = "poverty"
		var clickedAxis = clickedSelection.attr("data-axis-name");
		console.log("current x-axis: ", clickedAxis);

		// The onclick events below take place only if the x-axis is inactive
		// Clicking on an already active axis will therefore do nothing
		if (isClickedSelectionInactive) {
			// Assign the clicked axis to the variable currentAxisLabelX
			currentAxisLabelX = clickedAxis;
			// Call findMinAndMax() to define the min and max domain values.
			findMinAndMax(currentAxisLabelX, currentAxisLabelY);
			// Set the domain for the x-axis
			xLinearScale.domain([xMin, xMax]);
			// Create a transition effect for the x-axis
			svg
				.select(".x-axis")
				.transition()
				// .ease(d3.easeElastic)
				.duration(1800)
				.call(bottomAxis);

			// Select all circles to create a transition effect, then relocate its horizontal location
			// based on the new axis that was selected/clicked
			d3.selectAll("circle").each(function() {
				d3
				.select(this)
				.transition()
				// .ease(d3.easeBounce)
				.attr("cx", function(data) {
					return xLinearScale(+data[currentAxisLabelX]);
				})
				.duration(1800);
			});
			// Select all circle-text to create a transition effect
			d3.selectAll(".circle-text").each(function(){
				d3
				.select(this)
				.transition()
				.attr("x", function(data, index) {
					return xLinearScale(+data[currentAxisLabelX])-6;
				})
				.duration(1800);
			});

			// Change the status of the axes. See above for more info on this function.
			xlabelChange(clickedSelection);
		}
	});

	d3.selectAll(".yaxis-text").on("click", function() {
		// Assign a variable to current axis
		var clickedSelection = d3.select(this);
		// "true" or "false" based on whether the axis is currently selected
		var isClickedSelectionInactive = clickedSelection.classed("yinactive");
		// console.log("this axis is inactive", isClickedSelectionInactive)
		// Grab the data-attribute of the axis and assign it to a variable
		// e.g. if data-axis-name is "poverty," var clickedAxis = "poverty"
		var clickedAxis = clickedSelection.attr("data-axis-name");
		console.log("current y-axis: ", clickedAxis);

		// The onclick events below take place only if the x-axis is inactive
		// Clicking on an already active axis will therefore do nothing
		if (isClickedSelectionInactive) {
			// Assign the clicked axis to the variable currentAxisLabelX
			currentAxisLabelY = clickedAxis;
			// Call findMinAndMax() to define the min and max domain values.
			findMinAndMax(currentAxisLabelX, currentAxisLabelY);
			// Set the domain for the y-axis
			yLinearScale.domain([0, yMax]);
			// Create a transition effect for the x-axis
			svg
				.select(".y-axis")
				.transition()
				// .ease(d3.easeElastic)
				.duration(1800)
				.call(leftAxis);

			// Select all circles to create a transition effect, then relocate its horizontal location
			// based on the new axis that was selected/clicked
			d3.selectAll("circle").each(function() {
				d3
				.select(this)
				.transition()
				// .ease(d3.easeBounce)
				.attr("cy", function(data) {
					return yLinearScale(+data[currentAxisLabelY]);
				})
				.duration(1800);
			});
			// Select all circle-text to create a transition effect
			d3.selectAll(".circle-text").each(function(){
				d3
				.select(this)
				.transition()
				.attr("y", function(data, index) {
					return yLinearScale(+data[currentAxisLabelY])+4;
				})
				.duration(1800);
			});
			// Change the status of the axes. See above for more info on this function.
			ylabelChange(clickedSelection);
		}
	});

});

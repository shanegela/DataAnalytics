// Get references to the tbody element, input field and button
var $tbody = document.querySelector("tbody");
var $thead = document.querySelector("thead");
var $date1 = document.querySelector("#date1");

// bubble_visualization and hbar_visualization are declared without var to create global variables

//initialize table
$(document).ready(function () {
	$('#data_table').DataTable( {
		data: [],
		columns: [
			{ title: "Name", data:"name" },
			{ title: "Ticker", data: "ticker" },
			{ title: "Market Value", data: "mval", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Change in Market Value", data: "cmval", render: function(number){return number? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Shares", data: "shares", render: function(number){return number? number.toLocaleString(): null} },
			{ title: "Change in Shares", data: "cshares", render: function(number){return number? number.toLocaleString(): null}}
		]
	});
	
	chart_visualization = d3plus.viz()
		.container("#chart")
		.data([])
		.type("bubbles")
		.id(["","name"])
		.depth(1)
		.size("shares")
		.color("")

});

// get available dates
var queryURL = "http://localhost:5000/api/v1.0/dates";
d3.json(queryURL, function(error, response) {
	if (error) return console.warn(error);
	setSelection(response);
});

// function to set date input to latest available file date
function setSelection(response) {
	var lastDate = "";
	for (var i = 0; i < response.length; i++) {
		var $option = document.createElement("option");
		date =  response[i].trim();
		$option.innerText =  date;
		$date1.appendChild($option);
		lastDate = date;
	}

	populateTable(lastDate);
	$date1.value = lastDate;
}

// click event handler to update data
function selectFileDateHandler(e) {
	populateTable(e.value);
}

// updates the data in the table and charts
function populateTable(date) {
	setRadioButtons(date);

	var queryURL = "http://localhost:5000/api/v1.0/positions/" + date;
	d3.json(queryURL, function(error, response) {

		if (error) return console.warn(error);

		holdings = [];
		for (var i=0; i < response.length; i++) {
			item = response[i];
			//console.log(item);
			holdings.push({
				"name": item[0],
				"ticker": item[1],
				"cusip": item[2],
				"mval": parseFloat(item[3]),
				"cmval":  parseFloat(item[4]),
				"shares":  parseFloat(item[5]),
				"cshares":  parseFloat(item[6])
			});
		}
		
		var datatable = $('#data_table').DataTable();
		datatable.clear();
		datatable.rows.add(holdings);
		datatable.draw();

		drawChart();
	});
}


function drawBubbleChart(data, value="shares") {
	chart_visualization
		.data(data)
		.type("bubbles")
		.id(["","name"])
		.depth(1)
		.size(value)
		.color("")
		.shape("circle")
		.draw();
}

function drawHorizontalBarChart(data, value="mval") {

	top10 = data.sort(function(a, b) { return b.mval - a.mval })
	.slice(0, 10);

	var order = top10.map(function(d){ return d[value]; });

	chart_visualization
		.data(top10)  // data to use with the visualization
		.type("bar")       // visualization type
		.id("name")         // key for which our data is unique on
		.text("name")       // key to use for display text
		.y({"scale": "discrete", "value": "name", "label": "Security Name"})         // key to use for y-axis
		.x({"value": value, "label":""})          // key to use for x-axis
		.order({
			"sort": "asc",
			"value": function(d) { return order.indexOf(d); }
		})
		.shape("square")
		.draw()             // finally, draw the visualization!
}

function setChartTitle(title, value) {
	switch (value) {
		case "mval":
			title += " Market Value";
			break;
		case "cmval":
			title += " Change in Market Value";
			break;
		case "shares":
			title += " Shares Held";
			break;
		default: //"cshares"
			title += " Change in Shares Held";
	}
	d3.select("#chartTitle").text(title);
}

function getChartTypeValue(){
	var chartTypeRadios = document.getElementsByName('chartTypeRadio');
	var chartValueRadios = document.getElementsByName('chartValueRadio');
	var chartType = 'bubble';
	for (var i = 0; i < chartTypeRadios.length; i++) {
		if (chartTypeRadios[i].checked) { chartType = chartTypeRadios[i].value }
	}
	var chartValue = 'mval';
	for (var i = 0; i < chartValueRadios.length; i++) {
		if (chartValueRadios[i].checked) { chartValue = chartValueRadios[i].value }
	}
	return {type: chartType, value: chartValue}
}

function drawChart(e) {
	var chart = getChartTypeValue();
	//console.log("chart type: ", chart.type, " chart value: ", chart.value);
	if (chart.type === "bar") {
		setChartTitle("Top 10 Securities by", chart.value);
		drawHorizontalBarChart(holdings, chart.value);
	} else {
		setChartTitle("Securities by", chart.value);
		drawBubbleChart(holdings, chart.value);
	}
}

function setRadioButtons(date) {
	var dateLimit = "2013-06-30"
	var radio2 = document.querySelector("#chartValueRadio2");
	var radio4 = document.querySelector("#chartValueRadio4");
	
	if (date <= dateLimit) {
		//console.log('disabled')
		radio2.disabled = true;
		radio4.disabled = true;
		var chart = getChartTypeValue();
		if (chart.value == "cmval") {
			var chartRadio1 = document.querySelector("#chartValueRadio1");
			charttRadio1.checked = true;
		}
		if (chart.value == "cshares") {
			var chartRadio3 = document.querySelector("#chartValueRadio3");
			chartRadio3.checked = true;
		}
	} else {
		radio2.disabled = false;
		radio4.disabled = false;
	}

}
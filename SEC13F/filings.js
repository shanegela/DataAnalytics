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
	
	bubble_visualization = d3plus.viz()
		.container("#bubble-chart")
		.data([])
		.type("bubbles")
		.id(["","name"])
		.depth(1)
		.size("shares")
		.color("")
		.title("Securities by Shares")

	hbar_visualization = d3plus.viz()
		.container("#hbar-chart")  // container DIV to hold the visualization
		.title("Top 10 Securities by Market Value")
		.data([])  // data to use with the visualization
		.type("bar")       // visualization type
		.id("name")         // key for which our data is unique on
		.text("name")       // key to use for display text
		.y({"scale": "discrete", "value": "name", "label": "Security Name"})         // key to use for y-axis
		.x({"value": "mval", "label": "Market Value"})          // key to use for x-axis

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
	var queryURL = "http://localhost:5000/api/v1.0/positions/" + date;
	d3.json(queryURL, function(error, response) {

		if (error) return console.warn(error);

		var holdings = [];
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

		var top10 = holdings.sort(function(a, b) { return b.mval - a.mval })
		.slice(0, 10);

		drawHorizontalBarChart(top10);

		drawBubbleChart(holdings);
	});
}

function drawBubbleChart(data) {
	bubble_visualization
		.data(data)
		.type("bubbles")
		.id(["","name"])
		.depth(1)
		.size("shares")
		.color("")
		.title("Securities by Shares")
		.draw();
}


function drawHorizontalBarChart(data) {
	var order = data.map(function(d){ return d.marketvalue; });

	hbar_visualization
		.title("Top 10 Securities by Market Value")
		.data(data)  // data to use with the visualization
		.type("bar")       // visualization type
		.id("name")         // key for which our data is unique on
		.text("name")       // key to use for display text
		.y({"scale": "discrete", "value": "name", "label": "Security Name"})         // key to use for y-axis
		.x({"value": "mval", "label": "Market Value"})          // key to use for x-axis
		.order({
			"sort": "asc",
			"value": function(d) { return order.indexOf(d); }
		})
		.draw()             // finally, draw the visualization!
}
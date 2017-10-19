
// Get references to the tbody element, input field and button
var $tbody = document.querySelector("tbody");
var $thead = document.querySelector("thead");
var $date1 = document.querySelector("#date1");

//initialize table styles
$(document).ready( function () {
	$('#data_table').DataTable( {
		data: [],
		columns: [
			{ title: "Name" },
			{ title: "CUSIP" },
			{ title: "Market Value" },
			{ title: "Shares" }
		]
	} );
} );


var queryURL = "http://localhost:5000/api/v1.0/dates";
d3.json(queryURL, function(error, response) {
	if (error) return console.warn(error);
	setSelection(response);
});

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

function selectFileDateHandler(e) {
	//console.log(`selected ${e.value}`);
	populateTable(e.value);
}

function populateTable(date) {
	var queryURL = "http://localhost:5000/api/v1.0/positions/" + date;
	d3.json(queryURL, function(error, response) {
		if (error) return console.warn(error);

		var chartData = [];
		var datatable = $('#data_table').DataTable();
		datatable.clear();
		datatable.rows.add(response);
		datatable.draw();
		
		for (var x in response) {
			console.log(response[x]);
			chartData.push({
				"name": response[x][0], 
				"cusip": response[x][1], 
				"mval": response[x][2], 
				"shares": response[x][3]
			});
		}

		drawBubbleChart(chartData);

	});
}

//------------------------------------------------------------
// D3 PLUS BUBBLE CHAR
// // instantiate d3plus
// var visualization = d3plus.viz()
// 	.container("#chart-mval")     // container DIV to hold the visualization
// 	.data(sample_data)     // data to use with the visualization
// 	.type("bubbles")       // visualization type
// 	.id(["group", "name"]) // nesting keys
// 	.depth(1)              // 0-based depth
// 	.size("value")         // key name to size bubbles
// 	.color("group")        // color by each group
// 	.draw();               // finally, draw the visualization!

// var sample_data = [
// 	{"value": 100, "name": "alpha", "group": "group 1"},
// 	{"value": 70, "name": "beta", "group": "group 2"},
// 	{"value": 40, "name": "gamma", "group": "group 2"},
// 	{"value": 15, "name": "delta", "group": "group 2"},
// 	{"value": 5, "name": "epsilon", "group": "group 1"},
// 	{"value": 1, "name": "zeta", "group": "group 1"}
// ];

function drawBubbleChart(data) {
	var visualization = d3plus.viz()
		.container("#chart-mval")
		.data(data)
		.type("bubbles")
		.id(["","name"])
		.depth(1)
		.size("shares")
		.color("")
		.draw();
}
var $date1 = document.querySelector("#date1");
var $date2 = document.querySelector("#date2");
var $top_chart = document.querySelector("#top_chart");
var $bot_chart = document.querySelector("#bottom_chart");
var $rng_chart = document.querySelector("#range_chart");
var $data_tbl = document.querySelector("#data_table");

//initialize table
$(document).ready(function () {
	$('#data_table').DataTable( {
		data: [],
		columns: [
			{ title: "Name", data:"name" },
			{ title: "Ticker", data: "ticker" },
			{ title: "Beginning Date", data:"file_date1"},
			{ title: "Ending Date", date:"file_date2"},
			{ title: "Beginning Market Value", data: "mval1", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Beginning Price", data: "price1", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Ending Market Value", data: "mval2", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Ending Price", data: "price2", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Beginning Shares", data: "shares1", render: function(number){return number? number.toLocaleString(): null} },
			{ title: "Ending Shares", data: "shares2", render: function(number){return number? number.toLocaleString(): null} },
			{ title: "Simple Rate of Return", data:"srr", render: function(number){return number? number.toLocaleString(undefined, { minimumFractionDigits: 2 }): null}},
		]
	});

	topchart_visualization = d3plus.viz()
	.container("#top_chart")
	.data([])
	.type("bar")
	.id(["name"])
	.text("name");

	botchart_visualization = d3plus.viz()
	.container("#bottom_chart")
	.data([])
	.type("bar")
	.id(["name"])
	.text("name");
});


// get available dates
var queryURL = "http://localhost:5000/api/v1.0/dates";
d3.json(queryURL, function(error, response) {
	if (error) return console.warn(error);
	setDateRange(response);
});

// function to set from and to date inputs
function setDateRange(response) {
	var lastDate = "";
	for (var i = 0; i < response.length; i++) {
		date = response[i].trim();
		
		var $option1 = document.createElement("option");
		var $option2 = document.createElement("option");
		$option1.innerText =  date;
		$option2.innerText =  date;
		$date1.appendChild($option1);
		$date2.appendChild($option2);
	}
	
	$date1.value = response[response.length-2].trim();
	$date2.value = response[response.length-1].trim();
}

function btnSubmitHandler() {
	var start_date = $date1.value;
	var end_date = $date2.value;
	var queryURL = "http://localhost:5000/api/v1.0/srr/" + start_date + "/" + end_date;
	d3.json(queryURL, function(error, response) {
		if (error) return console.warn(error);
		
		holdings = [];
		for (var i=0; i < response.length; i++) {
			item = response[i];
			console.log(item);
			holdings.push(item);
		}

		var datatable = $('#data_table').DataTable();
		datatable.clear();
		datatable.rows.add(holdings);
		datatable.draw();
	
		drawCharts();
	
	});
}

function drawCharts() {

	top10 = holdings.sort(sort_order(false)).slice(0, 10);
	bot10 = holdings.sort(sort_order(true)).slice(0, 10);

	var top_order = top10.map(function(d){ return d["srr"]; });
	var bot_order = bot10.map(function(d){ return d["srr"]; });

	topchart_visualization
		.data(top10)  // data to use with the visualization
		.x({"value": "srr", "label":""})
		.y({"scale": "discrete", "value": "name", "label": "Security Name"})
		.shape("square")
		.order({
			"sort": "asc",
			"value": function(d) { return top_order.indexOf(d); }
		})
		.draw();

	botchart_visualization
		.data(bot10)  // data to use with the visualization
		.x({"value": "srr", "label":""})
		.y({"scale": "discrete", "value": "name", "label": "Security Name"})
		.shape("square")
		.order({
			"sort": "asc",
			"value": function(d) { return bot_order.indexOf(d); }
		})
		.draw();

}

var sort_order = function(ascending){
	
	  return function(a,b){ 
	
		if(a["srr"] === null){
		  return 1;
		}
		else if(b["srr"]=== null){
		  return -1;
		}
		else if(a["srr"] === b["srr"]){
		  return 0;
		}
		else if(ascending) {
		  return a["srr"] < b["srr"] ? -1 : 1;
		}
		else if(!ascending) {
		  return a["srr"] < b["srr"] ? 1 : -1;
		}
	  };
	}
	
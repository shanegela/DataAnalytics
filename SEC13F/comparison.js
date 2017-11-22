var $date1 = document.querySelector("#date1");
var $date2 = document.querySelector("#date2");
var $top_chart = document.querySelector("#top_chart");
var $bot_chart = document.querySelector("#bottom_chart");
var $rng_chart = document.querySelector("#range_chart");
var $data_tbl = document.querySelector("#data_table");
var $errmsg = document.querySelector("#errmsg");

//initialize table
$(document).ready(function () {

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

	linechart_visualization = d3plus.viz()
	.container("#line_chart")
	.data([])
	.type("line");

});


// get available dates
var queryURL = "https://sec13f-flask-heroku.herokuapp.com/api/v1.0/dates";
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
	if (start_date > end_date) {
		$errmsg.innerText ="The from date must be prior to the to date.";
		$errmsg.style.display = "block";
		$errmsg.style.color = "red";
	} else {
		$errmsg.innerText = "";
		$errmsg.style.display = "none";
		var queryURL = "https://sec13f-flask-heroku.herokuapp.com/api/v1.0/srr/" + start_date + "/" + end_date;
		d3.json(queryURL, function(error, response) {
			if (error) return console.warn(error);
			
			holdings = [];
			$.each(response, function(index, item) {
				holdings.push({
					"name": item.name,
					"ticker": item.ticker,
					"file_date1": item.file_date1,
					"file_date2": item.file_date2,
					"mval1": item.mval1,
					"price1": item.price1,
					"mval2": item.mval2,
					"price2": item.price2,
					"shares1": item.shares1,
					"shares2": item.shares2,
					"srr": item.srr
				})
			})

			drawCharts();
	
		});

		var queryURL2 = "https://sec13f-flask-heroku.herokuapp.com/api/v1.0/positions/" + start_date + "/" + end_date;

		d3.json(queryURL2, function(error, response) {
			if (error) return console.warn(error);

			var fdate = function(odate) {
				year = odate.substring(0,4);
				month = odate.substring(5,7);
				day = odate.substring(8,10);
				return "\"" + month + "/" + day + "/" + year + "\""
			}
			allholdings = [];
			$.each(response, function(index, item) {
				allholdings.push({
					"name": item.name,
					"ticker": item.ticker,
					"file_date": item.file_date,
					"mval": +item.mval,
					"price": +item.price,
					"shares": +item.shares
				})
			})

			drawChart();

		});
	}
}

function drawLineChart(data, value="mval") {
	var yLabel = "";
	if (value === "mval") {
		yLabel = "Market Value";
	}
	else if (value === "shares") {
		yLabel = "Shares Held";
	}
	else {
		yLabel = "Price";
	}

	linechart_visualization
		.data(data)
		.type("line")
		.id("ticker")
		.text("name")
		.y({"value": value, "label":yLabel})
		.x({"value": "file_date", "label": "File Date"})
		.draw();
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

function getLineChartValue(){
	var lineChartValueRadios = document.getElementsByName('lineChartValueRadio');
	var chartValue = 'mval';
	for (var i = 0; i < lineChartValueRadios.length; i++) {
		if (lineChartValueRadios[i].checked) { chartValue = lineChartValueRadios[i].value }
	}
	return chartValue
}

function drawChart(e) {
	var value =  getLineChartValue();
	drawLineChart(allholdings,value);
}

function setLineChartTitle(title, value) {
	switch (value) {
		case "mval":
			title += " Market Value Over Time";
			break;
		case "shares":
			title += " Shares Held Over Time";
			break;
		default: //"price"
			title += " Price Over Time";
	}
	d3.select("#lineChartTitle").text(title);
}

var $date1 = document.querySelector("#date1");
var $date2 = document.querySelector("#date2");

var $rng_chart = document.querySelector("#range_chart");
var $errmsg = document.querySelector("#errmsg");

//initialize table
$(document).ready(function () {

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
	console.log(response)
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
	
	$date1.value = response[response.length-5].trim();
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
		//var queryURL = "http://localhost:5000/api/v1.0/indsec/" + start_date + "/" + end_date;
		var type = getLineChartType();
		var queryURL = "https://sec13f-flask-heroku.herokuapp.com/api/v1.0/indsec/" + start_date + "/" + end_date;
		if (type == "indgrp") {
			queryURL = "https://sec13f-flask-heroku.herokuapp.com/api/v1.0/indgrp/" + start_date + "/" + end_date;
		}
		//console.log(queryURL)
		d3.json(queryURL, function(error, response) {
			if (error) return console.warn(error);
			
			holdings = [];
			$.each(response, function(index, item) {
				if (type == "indgrp") {
					holdings.push({
						"file_date": item.file_date,
						"indgrp": item.indgrp,
						"mval": item.mval,
						"shares": item.shares
					});	
				} else {
					holdings.push({
						"file_date": item.file_date,
						"indsec": item.indsec,
						"mval": item.mval,
						"shares": item.shares
					});	
				}
			})
			holdings.sort(compareFileDate);
			//console.log(holdings);
			drawChart();
	
		});
	}
}

function drawLineChart(data, type="indsec", value="mval") {
	var yLabel = "Industry Sector"
	if (type == "indgrp")
		yLabel = "Industry Group"
	setLineChartTitle(type, value);

	linechart_visualization
		.data(data)
		.type("line")
		.id(type)
		.text(type)
		.y({"value": value, "label":yLabel})
		.x({"value": "file_date", "label": "File Date"})
		.draw();
}

function getLineChartType(){
	var lineChartValueRadios = document.getElementsByName('lineChartTypeRadio');
	var chartValue = 'indsec';
	for (var i = 0; i < lineChartValueRadios.length; i++) {
		if (lineChartValueRadios[i].checked) { chartValue = lineChartValueRadios[i].value }
	}
	return chartValue
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
	var value = getLineChartValue();
	var type = getLineChartType();
	drawLineChart(holdings,type,value);
}

function setLineChartTitle(type, value) {
	var title = "Industry Sector by ";
	if (type == "indgrp") {
		title = "Industry Group by ";
	}

	if (value == "mval") {
		title += "Market Value Over Time";
	} else {
		title += "Shares Held Over Time";
	}

	d3.select("#lineChartTitle").text(title);
}

function compareFileDate(a,b) {
	return (a.file_date < b.file_date) ? -1 : (a.file_date > b.file_date) ? 1 : 0;
 }

 function drawChart(e) {
	var value = getLineChartValue();
	var type = getLineChartType();
	console.log(value, type);
	drawLineChart(holdings, type, value);
}
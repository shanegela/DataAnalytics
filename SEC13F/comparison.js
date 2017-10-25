var $date1 = document.querySelector("#date1");
var $date2 = document.querySelector("#date2");

//initialize table
$(document).ready(function () {
	$('#data_table').DataTable( {
		data: [],
		columns: [
			{ title: "Name", data:"name" },
			{ title: "Ticker", data: "ticker" },
			{ title: "Simple Rate of Return", data:"srr", render: function(number){return number? number.toLocaleString(undefined, { minimumFractionDigits: 2 }): null}},
			{ title: "Price", data:"price", render: function(number){return number? number.toLocaleString(undefined, { minimumFractionDigits: 2 }): null}},
			{ title: "Prior Price", data:"pprice", render: function(number){return number? number.toLocaleString(undefined, { minimumFractionDigits: 2 }): null}},
			{ title: "Market Value", data: "mval", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Change in Market Value", data: "cmval", render: function(number){return number? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Shares", data: "shares", render: function(number){return number? number.toLocaleString(): null} },
			{ title: "Change in Shares", data: "cshares", render: function(number){return number? number.toLocaleString(): null}}
		]
	});
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
			//console.log(item);
			holdings.push(item);
		}

		var datatable = $('#data_table').DataTable();
		datatable.clear();
		datatable.rows.add(holdings);
		datatable.draw();
	});
}

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

	// console.log(response);
	console.log("url", response);
	for (var i = 0; i < response.length; i++) {
		var $option = document.createElement("option");
		$option.innerText =  response[i].trim();
		$date1.appendChild($option);
	}
})

function populateTable(e) {
	//console.log(`selected ${e.value}`);

	var queryURL = "http://localhost:5000/api/v1.0/positions/" + e.value;
	d3.json(queryURL, function(error, response) {
		if (error) return console.warn(error);

		var datatable = $('#data_table').DataTable();
		datatable.clear();
		datatable.rows.add(response);
		datatable.draw();
	})

}

//initialize table
$(document).ready(function () {
	$('#aapl_data_table').DataTable( {
		data: [],
		columns: [
			{ title: "File Date", data:"file_date" },
			{ title: "Market Value", data: "mval", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Change in Market Value", data: "cmval", render: function(number){return number? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Shares", data: "shares", render: function(number){return number? number.toLocaleString(): null} },
			{ title: "Change in Shares", data: "cshares", render: function(number){return number? number.toLocaleString(): null}}
		]
	});
});

$(document).ready(function () {
	$('#ibm_data_table').DataTable( {
		data: [],
		columns: [
			{ title: "File Date", data:"file_date" },
			{ title: "Market Value", data: "mval", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Change in Market Value", data: "cmval", render: function(number){return number? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Shares", data: "shares", render: function(number){return number? number.toLocaleString(): null} },
			{ title: "Change in Shares", data: "cshares", render: function(number){return number? number.toLocaleString(): null}}
		]
	});
});


$(document).ready(function () {
	$('#cshares_data_table').DataTable( {
		data: [],
		columns: [
			{ title: "Name", data:"name" },
			{ title: "Ticker", data: "ticker" },
			{ title: "File Date", data:"file_date" },
			{ title: "Market Value", data: "mval", render: function(number){return number ? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Change in Market Value", data: "cmval", render: function(number){return number? number.toLocaleString("en-US", { style: "currency", currency: "USD" }): null} },
			{ title: "Shares", data: "shares", render: function(number){return number? number.toLocaleString(): null} },
			{ title: "Change in Shares", data: "cshares", render: function(number){return number? number.toLocaleString(): null}}
		]
	});
});

// updates the data in the table
function populateTables() {

	var queryURL = "https://sec13f-flask-heroku.herokuapp.com/api/v1.0/ticker/aapl"
	d3.json(queryURL, function(error, response) {

		if (error) return console.warn(error);

		holdings = [];
		for (var i=0; i < response.length; i++) {
			item = response[i];
			console.log(item);
			holdings.push({
				"file_date": item.file_date,
				"mval": parseFloat(item.mval),
				"cmval":  parseFloat(item.cmval),
				"shares":  parseFloat(item.shares),
				"cshares":  parseFloat(item.cshares),
				"price": parseFloat(item.price)
			});
		}
		console.log(holdings)
		
		var datatable = $('#aapl_data_table').DataTable();
		datatable.clear();
		datatable.rows.add(holdings);
		datatable.draw();
	});

	var queryURL = "https://sec13f-flask-heroku.herokuapp.com/api/v1.0/ticker/ibm"
	d3.json(queryURL, function(error, response) {

		if (error) return console.warn(error);

		holdings = [];
		for (var i=0; i < response.length; i++) {
			item = response[i];
			console.log(item);
			if (item.file_date > '2016-03-31') {
				holdings.push({
					"file_date": item.file_date,
					"mval": parseFloat(item.mval),
					"cmval":  parseFloat(item.cmval),
					"shares":  parseFloat(item.shares),
					"cshares":  parseFloat(item.cshares),
					"price": parseFloat(item.price)
				});
			}
		}
		console.log(holdings)
		
		var datatable = $('#ibm_data_table').DataTable();
		datatable.clear();
		datatable.rows.add(holdings);
		datatable.draw();
	});

	var queryURL = "https://sec13f-flask-heroku.herokuapp.com/api/v1.0/cshares/negative/2016-03-31"
	d3.json(queryURL, function(error, response) {

		if (error) return console.warn(error);

		csholdings = [];
		for (var i=0; i < response.length; i++) {
			item = response[i];
			console.log(item);
			csholdings.push({
				"file_date": item.file_date,
				"name": item.name,
				"ticker": item.ticker,
				"mval": parseFloat(item.mval),
				"cmval":  parseFloat(item.cmval),
				"shares":  parseFloat(item.shares),
				"cshares":  parseFloat(item.cshares),
				"price": parseFloat(item.price)
			});
		}
		console.log(csholdings)
		
		var csdatatable = $('#cshares_data_table').DataTable();
		csdatatable.clear();
		csdatatable.rows.add(csholdings);
		csdatatable.draw();
	});
}

populateTables()
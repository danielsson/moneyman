$(document).ready(function() {
	var myChart = new xChart('bar', type_spending, '#catSpenditure');
	
	$.each(type_histograms, function(index, value) {
		//Skip type 0:
		if(index === 0) return true;

		new xChart('line', value, '#type' + index + 'History');
	});
});
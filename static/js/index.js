$(document).ready(function() {
	var myChart = new xChart('bar', type_spending, '#catSpenditure');
	

	new xChart('line', type_histograms[1], '#takeAwayHistory');
	new xChart('line', type_histograms[2], '#clothesHistory');
	new xChart('line', type_histograms[3], '#coffeHistory');
	new xChart('line', type_histograms[4], '#aptHistory');
	new xChart('line', type_histograms[5], '#beerHistory');
	new xChart('line', type_histograms[6], '#depositHistory');
	new xChart('line', type_histograms[7], '#otherHistory');
});
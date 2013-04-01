$(document).ready(function() {
	var myChart = new xChart('bar', type_spending, '#catSpenditure');

	new xChart('line', type_histograms[0], '#takeAwayHistory');
	new xChart('line', type_histograms[1], '#clothesHistory');
	new xChart('line', type_histograms[2], '#coffeHistory');
	new xChart('line', type_histograms[3], '#aptHistory');
	new xChart('line', type_histograms[4], '#beerHistory');
	new xChart('line', type_histograms[5], '#depositHistory');
	new xChart('line', type_histograms[6], '#otherHistory');
});
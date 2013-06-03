

$(document).ready(function() {

	var timespans = MoneyMan.TimeUtils.getTimeSpans();

	var state = new MoneyMan.ViewState();
	var detailChart = new MoneyMan.DetailChart(state, MoneyMan.HistoryChartApi);
	detailChart.setState(state);

	var $btnTypes = $('#navTypes').find('a');

	$btnTypes.eq(0).parent().addClass('active');

	$btnTypes.click(function(e) {
		$this = $(this);
		e.preventDefault();

		$this.parent().addClass('active').siblings().removeClass('active');

		state.set(parseInt($this.attr('data-typeid')), null, null);
	});

	var $periodSelector = $('#selectPeriod');

	$periodSelector.change(function() {
		var span = timespans[$(this).val()];
		window.span = span;
		state.set(null, span.start, span.stop);
	});


	if(window.location.hash.length) {
		var parts = window.location.hash.substr(1).split(",");
		try {
			state.set(parts[0] || state.type, parts[1] || state.start, parts[2] || state.stop)

			$btnTypes.eq(state.type).parent().addClass('active').siblings().removeClass('active');
		} catch (e) {
			state = new MoneyMan.ViewState();
			console.log(e)
		}

	}

	detailChart.load();

});
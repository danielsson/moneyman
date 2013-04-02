

$(document).ready(function() {

	function setState(t,l,d) {
		state.set(t,l,d);

		detailChart.load();
	}

	var state = new MoneyMan.ChartState();
	var detailChart = new MoneyMan.DetailChart(state);

	$btnTypes = $('#navTypes').find('a');

	$btnTypes.eq(0).parent().addClass('active');

	$btnTypes.click(function(e) {
		$this = $(this);
		e.preventDefault();

		$this.parent().addClass('active').siblings().removeClass('active');

		setState(parseInt($this.attr('data-typeid')), false, false);
	});

	$periodSelector = $('#selectPeriod');

	$periodSelector.change(function() {
		$this = $(this);

		parts = $this.val().split(',');

		setState(false, parseInt(parts[0]), parseInt(parts[1]));
	});


	if(window.location.hash.length) {
		parts = window.location.hash.substr(1).split(",");
		try {
			state.set(parts[0] || state.type, parts[1] || state.len, parts[2] || state.duration)

			$btnTypes.eq(state.type).parent().addClass('active').siblings().removeClass('active');
		} catch (e) {
			state = new ChartState();
			detailChart.state = state;
			console.log(e)
		}

	}

	detailChart.load();

});
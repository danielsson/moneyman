$(document).ready(function() {

	var state = new MoneyMan.ChartState();
	var chart;

	function setState(t,l,d) {
		state.set(t,l,d);

		MoneyMan.TypeChartApi.dataFromState(state, function(data) {
			d3.select("#piechart svg")
				.datum(data.results)
				.transition().duration(1200)
				.call(chart);
		})

		
	}


	$periodSelector = $('#selectPeriod');

	$periodSelector.change(function() {
		$this = $(this);

		parts = $this.val().split(',');

		setState(false, parseInt(parts[0]), parseInt(parts[1]));
	});

	nv.addGraph(function() {
	  chart = nv.models.pieChart()
	      .x(function(d) { return d.label })
	      .y(function(d) { return d.value })
	      .showLabels(true)
	      .donut(true);

	  return chart;
	});

	setState()
});
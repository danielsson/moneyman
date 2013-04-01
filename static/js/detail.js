var DetailChart = function(s) {
	this.chart = null;
	this.state = s;
	
	var defaultElement = "#detailChart";
	var element = null;

	this.setElement = function(elem) {element = elem;};

	this.init = function(data, elem) {
		elem = elem || defaultElement;

		var opts = {
  			"dataFormatX": function (x) { return d3.time.format('%Y-%m-%d').parse(x); },
  			"tickFormatX": function (x) { return d3.time.format('%a %d %b')(x); }
		};

		this.chart = new xChart('line', data, elem, opts);
		element = elem;

		var r = this;
		this.chart.click = function() {r.onClick(this)};
	};

	this.setData = function(data) {

		if (this.chart === null) {
			this.init(data, element);
		} else {
			this.chart.setData(data);
		}
	};

	this.onClick = function() {};

	this.load = function() {
		var t = this;
		HistoryChartApi.getDataForState(this.state, function(data) {
			t.setData(data);
		});
	}

};

var ChartState = function(t,l,d) {
	this.type = t || 1;
	this.len = l || 7;
	this.duration = d || 86400;
}


var HistoryChartApi = (function() {
	var base = "/api/stats/history"

	this.getDataForState = function(state, callback) {
		var url = [base, state.type, state.len, state.duration].join('/');
		$.getJSON(url, callback);
	}
	return this;

})();

function setState(t,l,d) {
	state.type = t || state.type;
	state.len = l || state.len;
	state.duration = d || state.duration;

	detailChart.load();
}

$(document).ready(function() {

	window.state = new ChartState();
	window.detailChart = new DetailChart(state);

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
			state.type = parts[0] || state.type;
			state.len = parts[1] || state.len;
			state.duration = parts[2] || state.duration;

			$btnTypes.eq(state.type - 1).parent().addClass('active').siblings().removeClass('active');
		} catch (e) {
			state = new ChartState();
			detailChart.state = state;
			console.log(e)
		}

	}

	detailChart.load();

});
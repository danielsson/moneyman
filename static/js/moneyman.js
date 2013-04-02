
var MoneyMan = (function() {
	return new function() {
		this.DetailChart = function(s) {
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
				MoneyMan.HistoryChartApi.dataFromState(this.state, function(data) {
					t.setData(data);
				});
			}
		};

		this.ChartState = function(t,l,d) {
			this.type = t || 0;
			this.len = l || 7;
			this.duration = d || 86400;
		};

		this.HistoryChartApi = new function() {
			var base = "/api/stats/history"

			this.dataFromState = function(state, callback) {
				var url = [base, state.type, state.len, state.duration].join('/');
				$.getJSON(url, callback);
			}
			return this;

		};
	};
})();

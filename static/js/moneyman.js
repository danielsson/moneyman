
var MoneyMan = (function() {
	return new function() {
		this.DetailChart = function(s, a) {
			this.chart = null;
			this.state = s;
			this.api = a;
			
			var defaultElement = "#detailChart";
			var element = null;

			this.setElement = function(elem) {element = elem;};

			this.init = function(data, elem) {
				elem = elem || defaultElement;

				var opts = {
					//"dataFormatX": function (x) { return d3.time.format('%Y-%m-%d').parse(new Date(x*1000)); },
					"tickFormatX": function (x) { return d3.time.format('%a %d %b')(new Date(x*1000)); }
				};

				this.chart = new xChart('bar', data, elem, opts);
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
				this.api.dataFromState(this.state, function(data) {
					t.setData(data);
				});
			}
		};

		this.ChartState = function(t,l,d) {

			this.set = function(t,l,d) {
				//Since t may be 0 special care must be taken
				if(t !== false && t !== undefined)
					this.type = t;

				this.len = l || this.len;
				this.duration = d || this.duration;
			}

			this.set(t || 0, l || 31, d || 86400);
		};

		this.HistoryChartApi = new function() {
			var base = "/api/stats/history"

			this.dataFromState = function(state, callback) {
				var url = [base, state.type, state.len, state.duration].join('/');
				$.getJSON(url, callback);
			}
			return this;

		};

		this.TypeChartApi = new function() {
			var base = "/api/stats/spending_by_type"

			this.dataFromState = function(state, callback) {
				var url = [base, state.len, state.duration].join('/');
				$.getJSON(url, callback);
			}
			return this;

		};

		this.HistogramApi = new function() {
			var base = "/api/stats/histogram"

			this.dataFromState = function(state, callback) {
				var url = [base, state.len, state.duration].join('/');
				$.getJSON(url, callback);
			}
			return this;

		};
	};
})();

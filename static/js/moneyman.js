
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

			this.setState = function(state) {
				this.state = state;
				var me = this;
				this.state.listen(function(s) {
					me.load();
				});
			}

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

		/**
		 * ChartState 2.0
		 */
		this.ViewState = function(type, start, stop) {
			var listeners = [];

			function nGet(val, default_) {
				return (val === null || val === undefined) ? default_ : val; 
			}

			this.set = function(type, start, stop) {

				this.type = nGet(type, this.type);
				this.start = nGet(start, this.start);
				this.stop = nGet(stop, this.stop);

				for (var i = listeners.length - 1; i >= 0; i--) {
					listeners[i](this);
				};
			}

			/**
			 * Listen for state changes.
			 * @param  {Function} fn The function to run.
			 */
			this.listen = function(fn) {
				listeners[listeners.length] = fn;
			}

			//Initialize
			this.set(
				nGet(type, 0),
				nGet(start, MoneyMan.TimeUtils.now() - MoneyMan.TimeUtils.MONTH),
				nGet(stop, MoneyMan.TimeUtils.now()));

		}

		this.HistoryChartApi = new function() {
			var base = "/api/stats/history";

			this.dataFromState = function(state, callback) {
				var url = [base, state.type, state.start, state.stop].join('/');
				$.getJSON(url, callback);
			}
			return this;

		};

		this.TypeChartApi = new function() {
			var base = "/api/stats/spending_by_type";

			this.dataFromState = function(state, callback) {
				var url = [base, state.len, state.duration].join('/');
				$.getJSON(url, callback);
			}
			return this;

		};

		this.HistogramApi = new function() {
			var BASE = "/api/stats/histogram";

			this.dataFromState = function(state, callback) {
				if(!state instanceof MoneyMan.ViewState) {
					throw new Exception("HistogramApi does only support ViewState");
				}
				var url = [BASE, state.type, state.start, state.stop].join('/');
				$.getJSON(url, callback);
			}
			return this;

		};

		this.TimeUtils = new function() {
			this.HOUR = 3600;
			this.DAY = this.HOUR * 24;
			this.WEEK = this.DAY * 7;
			this.MONTH = this.DAY * 31;
			this.YEAR = this.DAY * 365;

			this.getTimeSpans = function () {
				return { //This is just beautiful...
			        "week": this.nowDelta(this.WEEK),
			        "month": this.nowDelta(this.MONTH),
			        "2months": this.nowDelta(2 * this.MONTH),
			        "6months": this.nowDelta(6 * this.MONTH),
			        "year": this.nowDelta(this.YEAR)
		    	};
		    };

			//Return now as unix timestamp in seconds
			this.now = function() {
				return parseInt((new Date()).getTime() / 1000);
			};

			/**
			 * Get a timespan between span ago and now
			 * @param  {[type]} span The timespan
			 * @return {[type]}      The timestamps as a dict.
			 */
			this.nowDelta = function(span) {
				var now = this.now();
				return {start: now - span, stop: now};
			};
		};
	};
})();

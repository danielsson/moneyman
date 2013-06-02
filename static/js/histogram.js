$(document).ready(function() {
    var timespans;

    timespans = { //This is just beautiful...
        "week": MoneyMan.TimeUtils.nowDelta(MoneyMan.TimeUtils.WEEK),
        "month": MoneyMan.TimeUtils.nowDelta(MoneyMan.TimeUtils.MONTH),
        "2months": MoneyMan.TimeUtils.nowDelta(2 * MoneyMan.TimeUtils.MONTH),
        "6months": MoneyMan.TimeUtils.nowDelta(6 * MoneyMan.TimeUtils.MONTH),
        "year": MoneyMan.TimeUtils.nowDelta(MoneyMan.TimeUtils.YEAR)
    };

    var state = new MoneyMan.ViewState();
    var detailChart = new MoneyMan.DetailChart(state, MoneyMan.HistogramApi);
    detailChart.setState(state);

    var $periodSelector = $('#selectPeriod'),
        $typeSelector = $('#selectType');

    $periodSelector.change(function() {
        var span = timespans[$(this).val()];

        state.set(null, span[0], span[1]);
    });

    $typeSelector.change(function() {
        state.set($(this).val(), null, null);
    });

    detailChart.load();
});
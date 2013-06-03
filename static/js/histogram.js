$(document).ready(function() {

    var timespans = MoneyMan.TimeUtils.getTimeSpans();

    var state = new MoneyMan.ViewState();
    var detailChart = new MoneyMan.DetailChart(state, MoneyMan.HistogramApi);
    detailChart.setState(state);

    var $periodSelector = $('#selectPeriod'),
        $typeSelector = $('#selectType');

    $periodSelector.change(function() {
        var span = timespans[$(this).val()];

        state.set(null, span.start, span.stop);
    });

    $typeSelector.change(function() {
        state.set($(this).val(), null, null);
    });

    detailChart.load();
});
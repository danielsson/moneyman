$(document).ready(function() {

	$rows = $('#transTable tbody tr')

	$rows.click(function() {
		$this = $(this);

		$("#transId").val($this.attr('data-id'));

		$("#adjustTypeModal").modal();
	});

});
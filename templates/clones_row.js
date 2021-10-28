$(function(){
	$('#addMore2').on('click', function() {
			var data = $("#tb2 tr:eq(1)").clone(true).appendTo("#tb2");
			data.find("input").val('');
	});
	$(document).on('click', '.remove', function() {
		var trIndex = $(this).closest("tr").index();
			if(trIndex>1) {
			$(this).closest("tr").remove();
		} else {
			
		}
	});
});  

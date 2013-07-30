$(document).ready(function() {
	Opentip.styles.tag = {
		extends: "standard",
  		showOn: 'mouseover', // this will disable the default <a /> link behaviour.
  		tipJoint: "bottom", // So the tooltip floats above the link
  		group: "tags" // Ensures that only one tag Opentip is visible
	};
	
	$('.project').each(function() {
		var tooltip = new Opentip($(this), {target: $(this), style: 'tag'});
		tooltip.setContent($(this).data('content'));
	});
});
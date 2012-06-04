jQuery(document).ready(function() {

    jQuery("#input_olduser").click(function() {
        jQuery('#user_inpu t').show();
    });

    jQuery("#input_newuser").click(function() {
        jQuery('#user_input').hide();
	});
	
	jQuery('.rpxnow').click(function(){
		RPXNOW.default_provider = this.id;
		return false;
	});

});

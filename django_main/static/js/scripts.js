$(function() {
    let click_function = function() {
        if  ($( this ).hasClass('disabled')) {
            return false;
        }
        $( this ).addClass('disabled');
        console.log( "click" );
        program_id = $( this ).attr('data-program-id');
        chart_label = $( this ).attr('data-chart-label');
        button = $( this );
        $.get( "/toggleToCompare?chart_label=" + chart_label + "&program_id=" + program_id, function( data ) {
          console.log(data['action'] === 'delete');
          console.log(data['action'] === 'add');
          console.log(data['action'])
          if (data['action'] === 'delete') {
            button.removeClass('enabled');
          } else if (data['action'] === 'add') {
            button.addClass('enabled');
          }
          button.removeClass('disabled');
        });
    }
    $('.toggleCompare').click(click_function);
});
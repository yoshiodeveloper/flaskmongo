var last_selected_from = null;
var last_selected_to = null;

function search_flights(form) {
    div = document.getElementById('result_id');
    $(div).fadeOut(250);
    $.ajax({
        url: form.action,
        method: 'GET',
        data: {
            'from': form.from_input.value,
            'to': form.to_input.value,
            'from_id': form.from_id.value,
            'to_id': form.to_id.value
        },
        cache: false,
        error: function(jqXHR, textStatus, errorThrown) {
            alert('Ocorreu um erro ao realizar a busca. Tente novamente mais tarde.');
        },
        success: function(data, jqXHR) {
            setTimeout(function() {
                $(div).html(data.html);
                $(div).fadeIn(250);
            }, 250);
        }
    });
}

function disable_flight(flight_id, el) {
    var flight = {'available': el.checked};
    $.ajax({
        url: '/flights/' + flight_id + '/save',
        method: 'POST',
        data: {'json': JSON.stringify(flight)},
        dataType: 'json',
        cache: false,
        error: function(jqXHR, textStatus, errorThrown) {
            alert('Ocorreu um erro ao realizar a alteração. Tente novamente mais tarde.');
        },
        success: function(data, jqXHR) {
            if (data.ok) {
                el.checked = data.flight.available;
            } else {
                alert(data.error);
            }
        }
    });
}

$(document).ready(function() {
    $('#from_input_id').autocomplete({
        serviceUrl: '/flights/check',
        params: {'direction': 'from'},
        autoSelectFirst: true,
        deferRequestBy: 100,
        noCache: true,
        onSearchStart: function(params) {
            if (params.query != last_selected_from) {
                document.getElementById('from_id').value = '';
                $('#to_input_id').attr('disabled', true);
            }
        },
        onSelect: function (suggestion) {
            last_selected_from = document.getElementById('from_input_id').value;
            document.getElementById('from_id').value = suggestion.data;
            $('#to_input_id').attr('disabled', false);
        }
    });
    $('#to_input_id').autocomplete({
        serviceUrl: '/flights/check',
        params: {'direction': 'to'},
        autoSelectFirst: true,
        deferRequestBy: 100,
        noCache: true,
        onSearchStart: function(params) {
            params.from_id = document.getElementById('from_id').value;
            if (params.query != last_selected_to)
                document.getElementById('to_id').value = '';
        },
        onSelect: function (suggestion) {
            last_selected_to = document.getElementById('to_input_id').value;
            document.getElementById('to_id').value = suggestion.data;
        }
    });
});
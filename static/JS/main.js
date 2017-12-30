var requests = $('#requests');

$.ajax({
    url: '/ajax/getRequests/',
    success: function (result) {

        requests.show();
        requests = requests.DataTable({
            "order": [[ 0, "desc" ]],
            "aaData": result,
            "aoColumns": [
                { "mDataProp": "request_id" },
                { "mDataProp": "api_name" },
                { "mDataProp": "input_params" },
                { "mDataProp": "date_added" },
                { "mDataProp": "status" },
                {
                    render: function (a, b, row_data) {
                        return row_data['status'] === 'Finished' ?
                            '<input type="button" value="std.out" class="stdout"/>  <input type="button" value="std.err" class="stderr"/>'
                            : '';
                    }
                },
                {
                    render: function (a, b, row_data) {
                        return row_data['status'] === 'Finished' ?
                            '<input type="button" value="Download Results" class="outputs"/>'
                            : '';
                    }
                }
            ],
            destroy: true
        });
    }
})
.done(function(){
    $("input[type='button']").on('click', function(){
        callDownloadUrl($(this))
    });
});

function callDownloadUrl(btn) {
    var row_data = requests.row( btn.parents('tr') ).data();
    var id = row_data['request_id'];
    switch (btn.attr('class')){
        case 'outputs':
            window.location.href = '/downloadResults/?request_id=' + id;
            break;

        case 'stdout':
            window.location.href = '/downloadLogs/?request_id=' + id + '&file=stdout';
            break;

        case 'stderr':
            window.location.href = '/downloadLogs/?request_id=' + id + '&file=stderr';
            break;
    }

}


$('#id_api_id').on('change', function () {
    getApiDescription($(this).val());
});


function getApiDescription(api_id){
    $.ajax({
        url: '/ajax/getApiDescription/',
        type: "GET",
        data: {'api_id': api_id},
        contentType: 'application/json',
        success: function(result){
            description = result['description'];
            $('#description-text').html(description);
        }
    });
}


$(document).ready(function () {
    getApiDescription($('#id_api_id').val())
});
$.ajax({
    url: '/ajax/getRequests/',
    success: function (result) {
        var requests = $('#requests');
        requests.show();
        requests.DataTable({
            "order": [[ 0, "desc" ]],
            "aaData": result,
            "aoColumns": [
                { "mDataProp": "request_id" },
                { "mDataProp": "api_name" },
                { "mDataProp": "input_params" },
                { "mDataProp": "date_added" },
                { "mDataProp": "status" },
                { "mDataProp": null },
                {
                    render: function (a, b, row_data) {
                        return row_data['status'] === 'Finished' ?
                            '<input type="button" id="'+row_data['request_id']+'" value="Download Results" class="script-download"/>'
                            : '';
                    }
                }
            ],
            destroy: true
        });
    }
})
.done(function(){
    $('.script-download').on('click', function(){
        window.location.href = '/downloadResults/?request_id=' + this.id;
    });
});
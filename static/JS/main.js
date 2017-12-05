$("#api-select").on('change', function(){
    if($(this).val() !== "None"){
        $.ajax({
            url: '/getAPIRequests/',
            data: {
                'api_id': $(this).val()
            },
            dataType: 'json',
            success: function (result) {
                var requests = $('#requests');
                if(!requests.is(":visible")){
                    requests.show()
                }
                requests.DataTable({
                    "aaData": result,
                    "aoColumns": [
                        { "mDataProp": "id" },
                        { "mDataProp": "api_name" },
                        { "mDataProp": "preferred_run_date" },
                        { "mDataProp": "params" },
                        { "mDataProp": "status" },
                        {
                            render: function (a, b, row_data) {
                                return row_data['status'] === 'scheduled' ?
                                    '<input type="button" id="'+row_data['id']+'" value="Run" class="script-run-btn"/>'
                                    : '';
                            }
                        }

                    ],
                    destroy: true
                });
            }
        })
        .done(function(){
            $('.script-run-btn').on('click', function(){
                $.ajax({
                    url: '/runRequest/',
                    data: {
                        'request_id': this.id
                    },
                    dataType: 'json',
                    success: function (result) {
                        alert(JSON.stringify(result))
                    }
                });
            });
        });
    }
});
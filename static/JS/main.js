$.ajax({
    url: '/ajax/getRequests/',
    success: function (result) {
        var requests = $('#requests');
        requests.show();
        requests.DataTable({
            "aaData": result,
            "aoColumns": [
                { "mDataProp": "request_id" },
                { "mDataProp": "api_name" },
                { "mDataProp": "input_params" },
                { "mDataProp": "date_added" },
                { "mDataProp": "status" },
                { "mDataProp": null },
                { "mDataProp": null }
                // {
                //     render: function (a, b, row_data) {
                //         return row_data['status'] === 'scheduled' ?
                //             '<input type="button" id="'+row_data['id']+'" value="Run" class="script-run-btn"/>'
                //             : '';
                //     }
                // }

            ],
            destroy: true
        });
    }
});
// .done(function(){
//     $('.script-run-btn').on('click', function(){
//         $.ajax({
//             url: '/runRequest/',
//             data: {
//                 'request_id': this.id
//             },
//             dataType: 'json',
//             success: function (result) {
//                 alert(JSON.stringify(result))
//             }
//         });
//     });
// });
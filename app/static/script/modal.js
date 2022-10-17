$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#car-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const carID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (carID === 'New car') {
            modal.find('.modal-title').text(carID)
            $('#car-form-display').removeAttr('carID')
        } else {
            modal.find('.modal-title').text('Edit car ' + carID)
            $('#car-form-display').attr('carID', carID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })


    $('#submit-car').click(function () {
        $.ajax({
            type: 'POST',
            url: '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'color': $('#car-modal').find('.dropdown-color').val(),
                'model': $('#car-modal').find('.dropdown-model').val(),
                'owner': $('#car-modal').find('.dropdown-owner').val()
            }),
            success: function (res) {
                console.log(res.success)
                if (res.success == false){
                    $("#errorModal").modal("toggle")
                }
                else{
                    location.reload();
                }
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#submit-owner').click(function () {
        $.ajax({
            type: 'POST',
            url: '/create_owner',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'owner_name': $('#owner-modal').find('.form-control').val(),
            }),
            success: function (res) {
                console.log(res.success)
                if (res.success == false){
                    $("#errorModal").modal("toggle")
                }
                else{
                    location.reload();
                }
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});
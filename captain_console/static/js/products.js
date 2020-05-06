$(document).ready(function(){
    $('#search-btn').on('click', function(e){
        e.preventDefault();
        const searchText = $('#search-box').val();
        $.ajax({
            url: '/products?search=' + searchText,
            type: 'GET',
            success: function(response){
                const newHTML = response.data.map(d => {
                    return `<div>

                            </div>`
                });
                $('#products').html(newHTML.join(''));
            },
            error: function(xhr, status, error){
                // TODO: Display error message (using toastr?)
                console.error(error);
            }
        });
    });
});
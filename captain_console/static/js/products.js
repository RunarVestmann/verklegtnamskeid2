$(document).ready(function(){
    $('#search-btn').on('click', function(e){
        e.preventDefault();
        const searchText = $('#search-box').val();
        $.ajax({
            url: '/products?search=' + searchText,
            type: 'GET',
            success: function(response){
                const newHTML = response.data.map(p => {
                    return `<div class="card" style="width: 18rem; background-color: #38b8c3; margin:1rem;">
                                <img class="card-img-top" src="${ p.first_image }" alt="Product image" style="height: 60%">
                                <div class="card-body">
                                    <h5 class="card-title">${ p.name }</h5>
                                    <p class="card-text">${ p.system.manufacturer } / ${ p.system.abbreviation } / ${ p.type }</p>
                                    <p>Verð: <strong>${ p.price }</strong> ISK</p>
                                    <a href="/products/${p.id}" class="btn btn-primary">Sjá nánar</a>
                                    <a href="#" class="btn btn-success">Setja í körfu</a>
                                </div>
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
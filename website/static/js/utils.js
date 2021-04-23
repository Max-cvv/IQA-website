function showModal(header, contain, button, url) {
    $('.modal-title').html(header);
    $('.modal-body').html(contain);
    if(button){
        $('.modal-footer').html('<a type="button" class="btn btn-primary" href ='+url+'>' + button +'</button>');
    }
    $("#myModal").modal();
}




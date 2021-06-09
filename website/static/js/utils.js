function showModal(header, contain, button, url) {
    $('#myModalLabel').html(header);
    $('#myModalBody').html(contain);
    if(button){
        $('#myModalFooter').html('<a type="button" class="btn btn-primary" href ='+url+'>' + button +'</button>');
    }
    $("#myModal").modal();
}




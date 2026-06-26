$(document).ready(function () {
    
    $('.btn-detalle').on('click', function() {
        $('#modal-id').text('#' + $(this).data('id'));
        $('#modal-nombre').text($(this).data('nombre'));
        $('#modal-email').text($(this).data('email'));
        $('#modal-telefono').text($(this).data('telefono'));
        $('#modal-fecha').text($(this).data('fecha'));
        $('#modal-hora').text($(this).data('hora'));
        $('#modal-personas').text($(this).data('personas'));
        $('#modal-estado').text($(this).data('estado'));
        $('#modal-token').text($(this).data('token'));
        $('#modal-qr').text($(this).data('qr'));
        $('#modal-creacion').text($(this).data('creacion'));
    });

});
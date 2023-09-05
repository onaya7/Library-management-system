$(document).ready(function(){
    $("#form-floating a").on('click', function(event){
        event.preventDefault();
        if($('#form-floating input').attr("type") == "text"){
            $('#form-floating input').attr('type', 'password');
            $('#form-floating i').addClass("fa-eye-slash");
            $('#form-floating i').removeClass("fa-eye");
        }else if($('#form-floating input').attr("type") == "password"){
            $('#form-floating input').attr('type', 'text');
            $('#form-floating i').removeClass("fa-eye-slash");
            $('#form-floating i').addClass("fa-eye");
        }
    });
});
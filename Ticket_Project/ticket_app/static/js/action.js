$(document).ready(function() {
    $("#register_text").click(function(){
        $("#register").toggle();
        $("#login").toggle();
        $(".card-title").html("Register");
    });
    $("#login_text").click(function(){
        $("#register").toggle();
        $("#login").toggle();
        $(".card-title").html("Login");
    });
    if($(".alert").html() != ''){
        setTimeout(function() {
            $(".alert").hide()
        }, 5000);
    }
});

function error_callback(data){
    alert(data.status);
}

function success_callback(data){
    console.log(data)
}

function login_success_callback(data){
        alert(data.token)
}

function login(){
    var username = $("#login_username").val();
    var password = $("#login_password").val();
    var url = "api/login/";
    ajaxPost(url, data={"username": username, "password": password}, 50000, login_success_callback, error_callback)
}
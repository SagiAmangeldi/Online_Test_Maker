function validateForm() {
    var username = document.forms["reg_form"]["username"].value;
    var password1 = document.forms["reg_form"]["password1"].value;
    var password2 = document.forms["reg_form"]["password2"].value;
    var engCharRegExp  = /^[a-z0-9]+$/i;
    if (!engCharRegExp.test(username)) {
        alert("тек латын әріптерін қолданыңыз \n пользуйтесь только латинскими буквами");
        return false;
    }
    if (username.length > 20) {
        alert("username 20 әріптен аз болуы тиіс \n username не может содержать больше 20 букв");
        return false;
    }
    if (!engCharRegExp.test(password1)) {
        alert("тек латын әріптерін қолданыңыз \n пользуйтесь только латинскими буквами");
        return false;
    }
    if (!engCharRegExp.test(password2)) {
        alert("тек латын әріптерін қолданыңыз \n пользуйтесь только латинскими буквами");
        return false;
    }
    return true;
}

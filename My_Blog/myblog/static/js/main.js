window.addEventListener("load", function() {

    // icono para mostrar contraseña
    showPassword = document.querySelector('.show-password');
    showPassword.addEventListener('click', () => {

        // elementos input de tipo clave
        password = document.querySelector('.password');

        if ( password.type === "text" ) {
            password.type = "password"
            showPassword.classList.remove('fa-eye-slash');
        } else {
            password.type = "text"
            showPassword.classList.toggle("fa-eye-slash");
        }

    })

});
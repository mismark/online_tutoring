const toggle=document.getElementById("togglePassword");

if(toggle){

    toggle.addEventListener("click",function(){

        const password=document.getElementById("id_password");

        if(password.type==="password"){

            password.type="text";

            toggle.innerHTML="🙈";

        }

        else{

            password.type="password";

            toggle.innerHTML="👁";

        }

    });

}
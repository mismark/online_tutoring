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




const imageInput=document.getElementById("imageInput");

if(imageInput){

imageInput.addEventListener("change",function(){

const file=this.files[0];

if(file){

document.getElementById("preview").src=URL.createObjectURL(file);

}

});

}
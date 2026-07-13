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


function togglePassword(){

let password=document.getElementById("password");

if(password.type==="password"){

password.type="text";

}

else{

password.type="password";

}

}




const imageInput = document.querySelector(
'input[type="file"]'
);

if(imageInput){

imageInput.addEventListener("change",function(){

const file=this.files[0];

if(file){

const reader=new FileReader();

reader.onload=function(e){

let preview=document.getElementById("preview");

if(preview){

preview.src=e.target.result;

}

}

reader.readAsDataURL(file);

}

});

}
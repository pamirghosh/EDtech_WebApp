const submit=document.getElementById("submit-btn")
const name_msg=document.querySelector(".nm");
const phone_msg=document.querySelector(".cn");
const email_msg=document.querySelector(".em");
const password_msg=document.querySelector(".pass");
const cpassword_msg=document.querySelector(".cp");
const add_msg=document.querySelector(".add");
const pass_check=document.querySelector("#pass-check");
const cpass_check=document.querySelector("#cpass-check");

//Show password if checkbox is tick
pass_check.addEventListener('change',()=>{
  let password=document.querySelector("#password");
  if(password.type=="password")
    password.type="text";
  else
    password.type="password";
});

//Show confirm password if checkbox is tick
cpass_check.addEventListener('change',()=>{
  let cpassword=document.querySelector("#cpassword");
  if(cpassword.type=="password")
    cpassword.type="text";
  else
    cpassword.type="password";
});

submit.addEventListener('click',()=>{
  name_msg.innerHTML="";
  phone_msg.innerHTML="";
  email_msg.innerHTML="";
  password_msg.innerHTML="";
  cpassword_msg.innerHTML="";
  add_msg.innerHTML="";
  document.querySelector('.sucess-msg').innerHTML="";

  event.preventDefault();
  let full_name=document.querySelector("#name").value;
  let phone=document.querySelector("#phone").value;
  let email=document.querySelector("#email").value;
  let password=document.querySelector("#password").value;
  let cpassword=document.querySelector("#cpassword").value;
  let address=document.querySelector("#address").value;
  let count=0;

  if(full_name==""){
    blankMessage("Name", name_msg);
    count++;
  }
  if(phone==""){
    blankMessage("Phone number", phone_msg);
    count++;
  }
  if(email==""){
    blankMessage("Email", email_msg);
    count++;
  }
  if(password==""){
    blankMessage("Password", password_msg);
    count++;
  }
  if(cpassword==""){
    blankMessage("Confirm password", cpassword_msg);
    count++;
  }
  if(address==""){
    blankMessage("Address", add_msg);
    count++;
  }
  //If all this attribute is validate
  if(phoneValidation(phone) && passwordValidation(password,cpassword) && checkEmail(email) && count==0){
    sendData(full_name, phone, email, password, address);
  }
});

//If any attribute is empty
function blankMessage(value, tag_name){
  tag_name.innerHTML=`<p>${value} can not be blank</p>`;
}

//For phone number validation
function phoneValidation(phone){
  if(phone.length==10){
    for(let i=0; i<phone.length; i++){
      if(phone.charCodeAt(i)<48 || phone.charCodeAt(i)>57){
        phone_msg.innerHTML=`<p>Phone number must contain digits only</p>`;
        return false;
      }else
        return true;
    }
  }
  else if(phone.length!=10){
    phone_msg.innerHTML=`<p>Phone number must contain 10 digits</p>`;
    return false;
  }
}

//For password validation
function passwordValidation(password, cpassword){
  if(password.length<8 || password.length>12){
    password_msg.innerHTML=`<p>Password must be between 8 to 12 charecter</p>`;
    return false;
  }
  else if(password!==cpassword){
    password_msg.innerHTML=`<p>Password and confirm password must be same</p>`;
    return false;
  }
  else{
    // Check weather the password contain atleast one uppercase, one lowercase and one numeric value.
    let upperChar=0;
    let lowerChar=0;
    let numericChar=0;
    for(let i=0; i<password.length; i++){
      if(password[i].charCodeAt(0)>=48 && password[i].charCodeAt(0)<=57)
        numericChar++;
      else if(password[i].charCodeAt(0)>=65 && password[i].charCodeAt(0)<=90)
        upperChar++;
      else if(password[i].charCodeAt(0)>=97 && password[i].charCodeAt(0)<122)
        lowerChar++;
    }
    if(upperChar>=1 && lowerChar>=1 && numericChar>=1)
      return true;
    else{
      password_msg.innerHTML=`<p>Password must include at least one uppercase letter, one lowercasex letter, and one number</p>`;
      return false;
    }
  }
}

//Check email is valid or not.
function checkEmail(email){
  let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if(!emailPattern.test(email)){
    email_msg.innerHTML=`<p>Provide a valid email address</p>`;
    return false;
  }
  else
    return true;
}

//Send data to backend
function sendData(full_name, phone, email, password, address){
  const data={
    full_name: full_name,
    phone:phone,
    password: password,
    email: email,
    address: address
  };

  fetch("/registration",{
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }).then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json(); 
  })
  .then(data => {
    const clsDiv=document.querySelector('#toggle');
      if(data==true){
        if(clsDiv.classList.contains('failue-msg')){
          clsDiv.classList.remove('failue-msg');
          clsDiv.classList.add('sucess-msg');
        }
        clsDiv.innerHTML='<p>Registration is done successfull</p>';
      }else{
        if(clsDiv.classList.contains('sucess-msg')){
          clsDiv.classList.remove('sucess-msg');
          clsDiv.classList.add('failue-msg');
        }
        clsDiv.innerHTML='<p>Email or Phone number is already exist</p>'
      }
  })
  .catch(error => {
      console.error('Error:', error); // Handle errors
  });
}
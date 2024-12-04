const login=document.querySelector('#login-btn');
const password_msg=document.querySelector(".pass");
const email_msg=document.querySelector(".em");

login.addEventListener('click',()=>{
  password_msg.innerHTML="";
  email_msg.innerHTML="";
  event.preventDefault();
  const email=document.querySelector('#email').value;
  const password=document.querySelector('#password').value;
  let inValidCount=0
  if(password==""){
    inValidCount++;
    blankMessage("Password", password_msg);
  }
  if(email==""){
    inValidCount++;
    blankMessage("Email", email_msg);
  }
  if(inValidCount==0){
    sendData(email,password);
  }
});

//If any attribute is empty
function blankMessage(value, tag_name){
  tag_name.innerHTML=`<p>${value} can not be blank</p>`;
}

function sendData(email, password) {
  let data = {
    email: email,
    password: password
  };
  fetch("/login_validation", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json(); 
  })
  .then(data => {
    let msg = document.querySelector("#toggle");
    if (!data.success) {
      msg.classList.remove('sucess-msg');
      msg.classList.add('failue-msg');   
      msg.innerHTML = `<p>${data.message}</p>`;
    } else {
      window.location.href = data.redirect_url;
    }
  })
  .catch(error => {
    console.error('Error:', error); 
  });
}

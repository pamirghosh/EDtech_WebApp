const container = document.querySelector('.container');

container.addEventListener('click', (e) => {
  if(e.target.classList.contains('payment')){
    const card = e.target.closest('.card-body');
    const courseName = card.querySelector('.course-name').
    innerHTML; 
    const price = card.querySelector('.price').innerHTML; 
    sendData(courseName, price); 
  }
});

function sendData(courseName, price) {
  let data = {
    courseName: courseName,
    price: price
  };
  fetch("/payment", {
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
    console.log(data) 
    const options = {
      "key": data['key_details'],
      "amount": data['order_details']['amount'],
      "currency": data['order_details']['currency'],
      "name": courseName,
      "description": "Product Description",
      "order_id": data['order_details']['id'],
      "handler": async function (response) {
          console.log("Sucess");
      }
    };
    const razorpay = new Razorpay(options);
    razorpay.open();
  })
  .catch(error => {
    console.error('Error:', error); 
  });
}

// document.addEventListener("DOMContentLoaded", function () {
//   document.querySelector('.php-email-form').addEventListener('submit', function (event) {
//       event.preventDefault(); // Prevent page reload

//       // Grab input values directly
//       let name = document.querySelector('input[name="name"]').value;
//       let email = document.querySelector('input[name="email"]').value;
//       let subject = document.querySelector('input[name="subject"]').value;
//       let message = document.querySelector('textarea[name="message"]').value;

//       let formData = new FormData();
//       formData.append("name", name);
//       formData.append("email", email);
//       formData.append("subject", subject);
//       formData.append("message", message);

//       fetch('http://127.0.0.1:8000/contact', {
//           method: 'POST',
//           body: formData
//       })
//       .then(response => response.json()) // Expect JSON response
//       .then(data => {
//           if (data.message === 'OK') {
//               alert('Message sent successfully!');
//               document.querySelector('.php-email-form').reset();
//           } else {
//               alert('Error: ' + (data.error || 'Form submission failed'));
//           }
//       })
//       .catch(error => {
//           alert('Error: ' + error.message);
//       });
//   });
// });

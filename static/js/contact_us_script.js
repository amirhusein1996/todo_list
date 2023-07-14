const contactUsForm = document.querySelector('.form-contact-us')

contactUsForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    var formData = $(contactUsForm).serialize();
    console.log(formData);

    $.ajax({
        url: '/contact-us/',
        type : 'POST',
        data: formData,
        success: function(response) {
            document.getElementById("changeable_section").innerHTML = response.html
            },
      error: function(xhr, status, error) {

        console.log(xhr.responseText);
      }
    })
  //   var formData = new FormData(e.target)
  //
  //   var jsonData = {}
  //   formData.forEach((value, key) => {
  //   jsonData[key] = value;
  // });
  //   console.log(jsonData)
  //   // axios.post('/contact-us/', jsonData).then(function (response){
  //   // console.log(response.data)
  //   //      // document.querySelector('.container').innerHTML = response.data.html
  //   // }).catch(function (error){
  //   //     console.log(error)
  //   // })
  //
  //   axios.post('/contact-us/', jsonData)
  // .then(function(response) {
  //   // Handle response
  //   console.log(response.data);
  // })
  // .catch(function(error) {
  //   // Handle error
  //   console.error(error);
  // });
})
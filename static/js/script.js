

///////////////////////////// Set CSRF Token to Header /////////////////////////////

// const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
// axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
$.ajaxSetup({
    headers: {"X-CSRFToken": $('meta[name="csrf-token"]').attr('content')}
})



///////////////////////////// Log Out /////////////////////////////
const logoutForm = document.getElementById("logoutForm")
const logoutLink = document.getElementById("logoutLink")

logoutLink.addEventListener('click' ,function (e){
    e.preventDefault();
    if (logoutForm.getAttribute('method').toLowerCase() === 'post'){
        logoutForm.submit()
    }
})
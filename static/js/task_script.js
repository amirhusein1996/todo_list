const filterFormBtn = document.querySelector('.col-md-4 .form-group .filter-form-btn')
const filterForm = document.querySelector(".col-md-4 .form-group .filter-form")
const toDoItemDiv = document.querySelector('.todo-list .todo-items')
const todoForm = document.getElementById("todoForm")
const todoFormAddBtn = todoForm.querySelector(".btn-primary")
const todoFormCancelBtn = todoForm.querySelector(".btn-secondary")
const todoFormTitle = document.querySelector('#title');
const todoFormDescription = document.querySelector('#description');
const todoFormPriority =  document.querySelector('#priority');
const todoFormCategory =  document.querySelector('#category');
const todoFormDeadline = document.querySelector('#dueDate');

let itemID
let item
let pageNumber // to keep the latest page clicked by user

//////////////////////////////// Editing ////////////////////////////////
function resetTodoForm(){
    // Reset the form inputs
  todoFormTitle.value = '';
  todoFormDescription.value = '';
  todoFormPriority.value = todoFormPriority.options[0].value;
  todoFormCategory.value = todoFormCategory.options[0].value;
  todoFormDeadline.value = '';

  // set itemID and item to null
    itemID = null
    item = null

  // Change the "Update" button back to an "Add" button
  todoFormAddBtn.textContent = 'Add';

  // Hide the "Cancel" button
  todoFormCancelBtn.style.display = 'none';
}

todoFormCancelBtn.addEventListener('click', ()=>{
    item.scrollIntoView({behavior:'smooth'})
    resetTodoForm()
})

function editThis(button , id) {

    // Scroll up to the form//
    window.scrollTo(0, 0);

    // asign itemID as a selected item
    itemID = id


    // Get the values of the todo item
    item = $(button).closest('.single-item').get(0); //.get method returns Javascript DOM instead of JQuery object
    const title = item.querySelector('.title').value;
    const description = item.querySelector('.description').value;
    const priority = item.querySelector('.priority').value;
    const category = item.querySelector('.category').value;
    const dueDate = item.querySelector('.deadline').value;

    // Fill the form with the values
    document.querySelector('#title').value = title;
    document.querySelector('#description').value = description;
    document.querySelector('#priority').value = priority;
    document.querySelector('#category').value = category;
    document.querySelector('#dueDate').value = dueDate;

    // Change the "Add" button to an "Update" button
    todoFormAddBtn.textContent = 'Update';

    // Show the "Cancel" button
    todoFormCancelBtn.style.display = 'inline-block';
}


todoFormAddBtn.addEventListener('click' , function (e){
    e.preventDefault()


    if (itemID){
        // if itemID exists , we send it to UpdateView
        var url = '/task/ajax/item/upadte/' + itemID
    }else {
        // if itemID doesn't exist , we send it to CreateView
        var url = '/task/ajax/item/create/'
    }

    var formData = $(todoForm).serialize()

   $.ajax({
  url: url,
  type: 'POST',
  data: formData
})
  .then(function(response) {
    if (response.data === true) {
      return $.ajax({
        url: '/task/ajax/todo-items/',
        type: 'GET',
        data: {'page' : pageNumber}
      });
    }
  })
  .then(function(response) {
      resetTodoForm()
    toDoItemDiv.innerHTML = response.data;
  })
  .catch(function(xhr, status, error) {
     console.error('Error:', xhr.responseText)
  });


})


function deleteThis(button , id){
    if (itemID || item){
        alert("You can't delete this while you're editing it")
        return
    }
    var singleItemDiv = $(button).closest(".single-item")
    $.ajax(
        {
            url : '/task/ajax/item/delete/' ,
            type : 'POST' ,
            data : {
                id : id
            },
            success:function (response){
                if (response.data === true){
                    singleItemDiv.remove()
                }
            }
        }
    )

}

function changeProgress(progressSelect, id){
    $.ajax(
        {
            url : '/task/ajax/item/update/progress/' ,
            data : {
                'progress' : progressSelect.value,
                'id' : id
            },
            type : "POST" ,
            success : function (response){
                // handle th success if needed
            },
            error : function (xhr, status, error) {
                alert(`Sorry, we were unable to update the progress for 
                ${$(progressSelect).closest(".single-item").find("h4").val()}.
                 Please try again later.`)
            }
        }
    )
}
//////////////////////////////// Filtering ////////////////////////////////
filterFormBtn.addEventListener('click',()=>{
    var formData = $(filterForm).serialize()



    $.ajax({
        url:'/task/ajax/todo-items/' ,
        type:'GET',
        data: formData,
        success: function (response) {
            toDoItemDiv.innerHTML = response.data
        },
        error : function (xhr, status, error) {



        }
    })
})


//////////////////////////////// Pagination ////////////////////////////////
function changePageNumber(page){
    pageNumber = page
    var formData = $(filterForm).serializeArray()
    formData.push({ name: "page", value: page });
    var serializedData = $.param(formData)


    $.ajax(
        {
            url:'/task/ajax/todo-items/' ,
            type:'GET',
            data: formData,
            success: function (response) {
                toDoItemDiv.innerHTML = response.data
            } ,
            error : function (xhr, status, error) {



        }
    })
}

//////////////////////////////// Searching ////////////////////////////////
const todoSearchForm = document.getElementById("todoSearchForm")

todoSearchForm.addEventListener('submit' , function (e){
    e.preventDefault()
    // check if search_query is empty , alert user
    if (!document.querySelector("input[type='search']").value){
        alert("Search box can't be empty")
        return
    }
    var formData = $(this).serializeArray()
    $.ajax(
        {
            url : '/task/ajax/todo-items/search/' ,
            data : formData ,
            type : 'GET' ,
            success : function (response){
                toDoItemDiv.innerHTML = response.data
                document.querySelector(".todo-list").scrollIntoView({behavior:'smooth' , block:'start'})
            },
            error : function (xhr, status, error) {



        }
        }
    )

})
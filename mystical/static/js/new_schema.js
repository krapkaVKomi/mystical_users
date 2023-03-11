
  // Find the container element and the "Add column" button
  const container = document.getElementById('container');
  const addButton = document.getElementById('addButton');

  // Initialize a counter for the number of clicks
  let clickCount = 0;

  // Add a click event listener to the "Add column" button
  addButton.addEventListener('click', function() {
    // Generate a unique identifier
    const id = `row${clickCount}`;

    // Increment the counter for the number of clicks
    clickCount++;

    // Create a new row of fields with unique IDs
    const newRow = document.createElement('div');
    newRow.classList.add('row');
    newRow.setAttribute('id', id);
    newRow.innerHTML = `
      <div class="col">
        <p>Column name</p>
        <input class="form-control" value="" id="${id}-columnName" type="text" name="${id}-columnName" maxlength="50" required>
      </div>
      <div class="col">
        <p>Type</p>
        <select id="${id}-type" name="${id}-type" class="form-control" required>
          <option value="" selected disabled hidden>-----</option>
          <option value="Name">Name</option>
          <option value="Job">Job</option>
          <option value="Email">Email</option>
          <option value="Domain name">Domain name</option>
          <option value="Phone number">Phone number</option>
          <option value="Company name">Company name</option>
          <option value="Text">Text</option>
          <option value="Integer">Integer</option>
          <option value="Date">Date</option>
        </select>
      </div>
      <div class="col" id="${id}-from-to-row">

      </div>
      <div class="col">
        <p>Order</p>
        <input type="number" class="form-control" value="${clickCount}" id="${id}-order" type="text" name="${id}-order" required>
      </div>
      <div class="col">
        <br><br><a style="color: red;" href="#" class="delete-link" data-rowid="${id}">Delete</a>
      </div>
      <div class="col">
    </div>
    `;

    // Append the new row to the container
    container.appendChild(newRow);

    // Add a click event listener to the delete link
    const deleteLink = newRow.querySelector('.delete-link');
    deleteLink.addEventListener('click', function(event) {
      event.preventDefault();
      const rowId = deleteLink.getAttribute('data-rowid');
      const row = document.getElementById(rowId);
      row.remove();
    });

    // Add a change event listener to the type select input
    const typeSelect = newRow.querySelector(`#${id}-type`);
    typeSelect.addEventListener('change', function() {
      const selectedValue = typeSelect.value;
      const fromToRow = newRow.querySelector(`#${id}-from-to-row`);

      console.log(selectedValue);

      if (selectedValue === 'Integer') {
    fromToRow.innerHTML = `
      <div class="row g-3">
        <div class="col">
          <p>From</p>
          <input type="number" class="form-control" placeholder="Start" value="start" name="${id}-start" required>
        </div>
        <div class="col">
          <p>To</p>
          <input type="number" class="form-control" placeholder="End" value="end" name="${id}-end" required>
        </div>
      </div>
    `;
  }
   else if (selectedValue === 'Text'){
    fromToRow.innerHTML = `
      <div class="row g-3">
        <div class="col">
          <p>Number</p>
          <input type="number" class="form-control" placeholder="number" value="number" name="${id}-number" required>
        </div>
      </div>
    `;
    }
   else {
    fromToRow.innerHTML = '';
  }
  });

});



const form = document.getElementById('myForm');

form.addEventListener('submit', function(event) {
  event.preventDefault(); // prevent the form from submitting normally

  const formData = new FormData(form); // get the form data

  // send the form data to the server using AJAX
  const xhr = new XMLHttpRequest();
  xhr.open('POST', form.action);
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // set the CSRF token header
  xhr.onload = function() {
    if (xhr.status === 200) {
      const response = JSON.parse(xhr.responseText); // parse the JSON response
      if (response.success) {
        // redirect the user to the appropriate URL based on the response
        const columnSchemaPk = response.column_schema_pk;
        window.location.href = `/generate_csv/${columnSchemaPk}/`;
      } else {
        alert('An error occurred.'); // display an error message
      }
    }
  };
  xhr.send(formData);
});

// helper function to get the value of a cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


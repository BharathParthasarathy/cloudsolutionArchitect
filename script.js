// Function to retrieve tokens from the URL and store them in localStorage

function getTokensFromURL() {

    // Check if the tokens have already been retrieved
    if (sessionStorage.getItem('tokensRetrieved')) {
       // Tokens already retrieved, return the stored tokens
       const idToken = sessionStorage.getItem('idToken');
       const accessToken = sessionStorage.getItem('accessToken');
       const tokenValue = idToken;
       return { accessToken, idToken, tokenValue };
   }
   const hashParams = new URLSearchParams(window.location.hash.substring(1));
   const accessToken = hashParams.get('access_token');
   const idToken = hashParams.get('id_token');
   tokenValue = idToken;
   sessionStorage.setItem('idToken', idToken);
   sessionStorage.setItem('accessToken', accessToken);
   sessionStorage.setItem('tokensRetrieved', true);
   return { accessToken, idToken, tokenValue  };
}

// Function to fetch books with token-based authentication
function fetchBooks() {
   const idToken = sessionStorage.getItem('idToken');
   console.log('ID Token:', idToken);
   if (!idToken) {
       // Display an error message in the UI
       const errorMessage = document.createElement('p');
       errorMessage.textContent = 'ID token not found. Please authenticate to access books.';
       document.getElementById('bookContainer').appendChild(errorMessage);
       return;
   }

   fetch('https://bfcvc1fh56.execute-api.us-east-1.amazonaws.com/newrestapistage/Get-items', {
       method: 'GET',
       headers: {
           'Authorization': `Bearer ${idToken}`
       }
   })
   .then(response => {
       if (!response.ok) {
           throw new Error('Network response was not ok');
       }
       return response.json();
   })
   .then(data => {
       // Process API response data and update UI
       const bookContainer = document.getElementById('bookContainer');
       bookContainer.innerHTML = '';

       data.forEach(book => {
           const tile = document.createElement('div');
           tile.classList.add('book-tile');

           for (let key in book) {
               const attribute = document.createElement('p');
               attribute.textContent = `${key}: ${book[key]}`;
               tile.appendChild(attribute);
           }

           const modifyButton = document.createElement('button');
           modifyButton.textContent = 'Modify';
           modifyButton.addEventListener('click', () => modifyBook(book.id));
           tile.appendChild(modifyButton);

           const deleteButton = document.createElement('button');
           deleteButton.textContent = 'Delete';
           deleteButton.addEventListener('click', () => deleteBook(book.id));
           tile.appendChild(deleteButton);

           bookContainer.appendChild(tile);
       });
   })
   .catch(error => {
       // Display an error message in the UI
       const errorMessage = document.createElement('p');
       errorMessage.textContent = 'User is not Authorized to View this Page ,Failed to fetch books.';
       document.getElementById('bookContainer').appendChild(errorMessage);
       console.error('API request failed:', error);
   });
}

// Call the function to store tokens when the page loads



// Function to add a book with token-based authentication
document.addEventListener('DOMContentLoaded', function() {
   // Add event listener for form submission
   const addBookForm = document.getElementById('addBookForm');
   addBookForm.addEventListener('submit', function(event) {
     event.preventDefault(); // Prevent default form submission behavior
     // Call addBook() function to handle form data
     addBook();
   });

function addBook() {
   const idToken = sessionStorage.getItem('idToken');
   // Get form input values
   const id = parseInt(document.getElementById('id').value);
   const Authors = document.getElementById('Authors').value;
   const Publisher = document.getElementById('Publisher').value;
   const Title = document.getElementById('Title').value;
   const Year =document.getElementById('Year').value;

   const jsonMessage = JSON.stringify({ id, Authors, Publisher, Title, Year});
   console.log("JSON message:", jsonMessage);
   // Perform validation if needed
   
 
   // Call your API endpoint to add the book
   fetch('https://bfcvc1fh56.execute-api.us-east-1.amazonaws.com/newrestapistage/post_item', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
       'Authorization': 'Bearer ' + idToken 
     },
     body: JSON.stringify({ id, Authors, Publisher, Title, Year})
   })
   .then(response => {
       if (response.ok) {
           // Clear the form
           document.getElementById('id').value = '';
           document.getElementById('Authors').value = '';
           document.getElementById('Publisher').value = '';
           document.getElementById('Title').value = '';
           document.getElementById('Year').value = '';

           alert('Book added successfully.');

           // Redirect back to home.html with token ID
           window.location.href = `home.html#id_token=${idToken}`;
       } else {
           alert('Failed to add book. Please try again.');
       }
   })
   .catch(error => {
       console.error('Error adding book:', error);
       alert('Failed to add book. Please try again.');
   });
}
});
// Function to delete a book with token-based authentication
async function deleteBook(bookId) {
   // Confirm deletion with the user
   console.log(`Delete book with ID ${bookId}`);
   if (confirm('Are you sure you want to delete this book?')) {
       try {
           // Create a JavaScript object with the book ID
           const data = { id: bookId };

           // Convert the JavaScript object to JSON format
           const jsonData = JSON.stringify(data);

           // Send a DELETE request with the JSON data to the Lambda function endpoint
           const response = await fetch(`https://bfcvc1fh56.execute-api.us-east-1.amazonaws.com/newrestapistage/delete-item`, {
               method: 'DELETE',
               headers: {
                   'Content-Type': 'application/json'
                   
               },
               body: jsonData
           });

           if (response.ok) {
               // Book deleted successfully, fetch and display updated book list
               fetchBooks();
               // Display confirmation message to the user
               window.alert('Book deleted successfully!');
           } else {
               throw new Error('Failed to delete book');
           }
       } catch (error) {
           console.error('Error deleting book:', error);
           alert('Failed to delete book. Please try again.');
       }
   }
}

// Function to modify a book with token-based authentication
async function modifyBook(id) {
   const idToken = sessionStorage.getItem('idToken');
   const response = await fetch(`https://bfcvc1fh56.execute-api.us-east-1.amazonaws.com/newrestapistage/getby-id?id=${id}`, {
       method: 'GET',
       headers: {
           'Content-Type': 'application/json'
           
       }
   });
   if (!response.ok) {
       throw new Error('Failed to fetch book details');
   }
   
   const responseBody = await response.json();
   console.log('Response Data:', responseBody);

   // Extract data from the response body
   const { id: bookId, Title, Publisher, Authors, Year } = JSON.parse(responseBody.body);
   const numericId = parseInt(bookId, 10);
   console.log('Extracted Data:', numericId, Title, Publisher, Authors, Year);

   window.location.href = `edit.html?id=${numericId}&Title=${encodeURIComponent(Title)}&Publisher=${encodeURIComponent(Publisher)}&Authors=${encodeURIComponent(Authors)}&Year=${encodeURIComponent(Year)}`;
   
} 


getTokensFromURL();
fetchBooks();

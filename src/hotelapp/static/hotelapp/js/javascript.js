// Constants
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const formElement = document.querySelector('form');
const resultsContainerElement = document.querySelector('.results_container');

// Eventlisteners
formElement.addEventListener('submit', filterHotelsByCity)

// Functions
async function filterHotelsByCity(event) {
   /**
   * Asynchronous function for making post request with passed in city filter.
   */
   event.preventDefault();
   const formData = new FormData(formElement);

   const response = await fetch('/', {
       method: 'POST',
       headers: {'X-CSRFToken': csrfToken},
       body: formData,
   });

   // Collect and parse the response html data
   const data = await response.text()
   const domParser = new DOMParser();
   const parsedHtml = domParser.parseFromString(data, 'text/html');

   // Replace the right html element with the parsed data
   resultsContainerElement.innerHTML = parsedHtml.querySelector('.results_container').innerHTML;
}

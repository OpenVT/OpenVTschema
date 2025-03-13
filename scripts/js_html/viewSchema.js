
const schema_div = "jsonSchema_div"
const schema_h2 = "schema_name_h2"

window.onload = function (){
    const urlParams = new URLSearchParams(window.location.search);
    const fileName = urlParams.get('schema_fileName');
    console.log(fileName); 
    displaySchema(fileName) 
    const fileName_ar = fileName.split("/")
    for(const element of fileName_ar) {
        if (element.includes(".json")) {
            const jsonFile_h2 = document.getElementById(schema_h2);
            jsonFile_h2.innerHTML = element;
        }
    }
    
}

async function displaySchema(jsonFile) {

    fetch(jsonFile)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const jsonDisplay = document.getElementById(schema_div);
        // Format the JSON data for better readability, indent 2 spaces:
        const formattedJson = JSON.stringify(data, null, 2);
        jsonDisplay.innerHTML = `<pre>${formattedJson}</pre>`;
      })
      .catch(error => {
        console.error('Error fetching or parsing JSON:', error);
        document.getElementById(schema_div).textContent = 'Failed to load JSON data.';
      });
}
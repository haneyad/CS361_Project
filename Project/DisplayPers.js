/*
    Function for formatting and sending HTTP Request when search is submitted
*/
function sendGET(){

    const xhr = new XMLHttpRequest();

    xhr.onload = () => {

    // print JSON response
    if (xhr.status >= 200 && xhr.status < 300) {
        // parse JSON
        const response = JSON.parse(xhr.responseText);
        createTables(response);
    }
};

let url = '/personals'; /* ENTER FULL SERVER URL HERE */

xhr.open('GET', url);

xhr.setRequestHeader('Content-Type', 'application/json');

xhr.send();

function sendGET(){

    const xhr = new XMLHttpRequest();

    xhr.onload = () => {

    // print JSON response
    if (xhr.status >= 200 && xhr.status < 300) {
        // parse JSON
        const response = JSON.parse(xhr.responseText);
        createTables(response);
    }
};

let url = '/personals'; /* ENTER FULL SERVER URL HERE */

xhr.open('GET', url);

xhr.setRequestHeader('Content-Type', 'application/json');

xhr.send();

}

/*
    Function for creating tables with data from JSON response
*/
function createTables(arrData){
    myTable = document.getElementById('searchResultsBody');
    myTable.innerHTML = "";
    
    let i = Math.floor(Math.random() * (arrData.length - 1));


    // Below dynamically add single row of data for display

    let newRow = document.createElement('tr');

    let newPosted = document.createElement('td');
    newPosted.innerText = arrData[i].last_update;

    let newDescription = document.createElement('td');
    newDescription.innerText = arrData[i].name;

    let newLocation = document.createElement('td');
    newLocation.innerText = arrData[i].location;

    let newLink = document.createElement('td');
    newLink.innerHTML = '<a href=' + String(arrData[i].url) + '>' + 'Link' + '</a>';
    console.log(newLink);
    
    newRow.append(newPosted, newDescription, newLocation, newLink);
    myTable.append(newRow);
}

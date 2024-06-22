
// requires search.js
//import {getOptions} from "./search.js";

// In search.js:
//const htmlObjTable = "objectTable";
//const htmlProcessTable = "processTable";

window.onload = function (){
  initTables(); 
}

async function initTables() {
  const procTableData = await getOptions("processes");
  fillOutTable(procTableData,"processes"); 
  const objTableData = await getOptions("objects")
  fillOutTable(objTableData, "objects");	
}

/**
 * Function to fill in an HTML table with data from frameworks schema
 * @param {frameworksMap, objectType} 
 *         frameworksMap - The Map that contains data for table.
 *         objectType - string with clue to id of the table to be filled out.
 * @returns {} - Nothing returned, fills out html table.
 */
async function fillOutTable(frameworksMap, objType) {
// TODO: since this fills out a specific HTML table, move it out of this file.
  let table;
  let columnTwoTag;
  if ( objType.includes("object")) {
	table = document.getElementById(htmlObjTable)
	columnTwoTag = "Attributes";
  }
  else { // 'process'
	table = document.getElementById(htmlProcessTable)
	columnTwoTag = "Description"
  }
  table.innerHTML = ""; // clear table
  
  const tblHeader = document.createElement("thead");
  const row = document.createElement("tr");
  const cell = document.createElement("th");
  const cellText = document.createTextNode("Name");
  cell.appendChild(cellText);
  row.appendChild(cell)
  const cell2 = document.createElement("th");
  const cellText2 = document.createTextNode(columnTwoTag);
  cell2.appendChild(cellText2);
  row.appendChild(cell2)
  
  tblHeader.appendChild(row);
  table.appendChild(tblHeader);
  
  const tblbody = document.createElement("tbody");
  
  const numRows = frameworksMap.size;
  for(const [key, value] of frameworksMap) {
    const row = document.createElement("tr");
	const cell = document.createElement("td");
    const cellText = document.createTextNode(key);
    cell.appendChild(cellText);
	row.appendChild(cell)
	const cell2 = document.createElement("td");
	let cellText2;
	if(columnTwoTag === "Attributes") { // Objects
	  let attributes = '';
	  for(let i =0; i<value.length;i++) {
		attributes = attributes + value[i] + " ";  
	  }		  
	  cellText2 = document.createTextNode(attributes);
	}
    else {cellText2 = document.createTextNode(value);} // Processes
    cell2.appendChild(cellText2);
    row.appendChild(cell2)
	
	tblbody.appendChild(row);
  }	  
  table.appendChild(tblbody);
	
}
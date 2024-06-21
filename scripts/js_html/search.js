// search functions

const frameworkNames = ["compucell3d.json","hal.json","morpheus.json","netlogo.json","physicell.json","polyhoop.json","simucell3d.json","tissue_forge.json","artistoo.json","biocellion.json","biodynamo.json","chaste.json"];
// TODO: have a script on GitHub that generates a list of framework json files that this reads instead
//       of hard coded array.

const htmlObjTable = "objectTable";
const htmlProcessTable = "processTable";

window.onload = function (){
  loadOptions ("processes", "processSelect")  
  loadOptions ("objects", "objectSelect")
}

async function loadOptions (optionTypeStr, htmlElementId) { 
   const newSelect = document.getElementById(htmlElementId);
   var optionMap = await getOptions(optionTypeStr);           
    
   for (let [key,value] of optionMap) {
	 var opt = document.createElement("option"); 
     opt.setAttribute("value", key); 
     var nod = document.createTextNode(key); 
     opt.appendChild(nod);	
     newSelect.appendChild(opt);	 
   }
	
}

async function processSelection(objType, selectionId) {
//console.log("Hi " + selectionId);
  const indexSelection = document.getElementById(selectionId).selectedIndex;
  const htmlOptions = document.getElementById(selectionId).options;
  const frameworksMap = await getFrameworksThatSupport(htmlOptions[indexSelection].text, objType); 
  console.log(frameworksMap);
  fillOutTable(frameworksMap, objType);
}

/**
  Return Map of objects with description that support object type.(processes, objects, boundries, etc )
*/
async function getOptions(typeStr) {
	const objectsMap = new Map();
	for(let i= 0; i< frameworkNames.length; i++) {
	//const jsonName = "artistoo.json"
	  const jsonName = frameworkNames[i];
	  const jsonURL = "simulator_schemas/"+ jsonName;
	  await fetch(jsonURL)
		 .then((response) => response.json())
		 .then((json) => {
	   //console.log(json);
		  const newobjs = json[typeStr];
		  for(const id in newobjs) {
		    //console.log(id+ ": "+ newobjs[id].name);
			if ( objectsMap.get(newobjs[id].name) == null) {// new object
			  if(typeStr.includes("object")) {
				objectsMap.set(newobjs[id].name,newobjs[id].attributes);  
			  }
			  else { objectsMap.set(newobjs[id].name,newobjs[id].description);} // process  
			}
		  }
	  });
	
	}
	return objectsMap;
}

/**
 * Function that gets frameworks that support a specific object (object can be any top-level name in schema)
 * @param {supportedObjStr, objTypeStr} 
 *         supportedObjStr - string with name of support that is searched for in each specific framework json file.
 *         objTypeStr - string with top level name in schema to look for support under.
 * @returns {frameworksMap} - Returns data from frameworks schema that support 'supportedObjStr'.
 */
async function getFrameworksThatSupport(supportedObjStr, objTypeStr) {
  const frameworksMap = new Map();
  for(let i= 0; i< frameworkNames.length; i++) {
	//const jsonName = "artistoo.json"
	  const jsonName = frameworkNames[i];
	  const jsonURL = "simulator_schemas/"+ jsonName;
	  await fetch(jsonURL)
		 .then((response) => response.json())
		 .then((json) => {
	   //console.log(json);
	 	  frameworkData = json;
		  const newobjs = frameworkData[objTypeStr];
		  for(const id in newobjs) {
		    //console.log(id+ ": "+ newobjs[id].name);
			if ( newobjs[id].name === supportedObjStr) {
			  frameworksMap.set(frameworkData.name,{description:frameworkData.description, url:frameworkData.website}); 
			}
		  }
	  });
	
	}
	return frameworksMap;
	
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
  if ( objType.includes("object")) {
	table = document.getElementById(htmlObjTable)
  }
  else {
	table = document.getElementById(htmlProcessTable)
  }
  table.innerHTML = ""; // clear table
  
  tblHeader = document.createElement("thead");
  const row = document.createElement("tr");
  const cell = document.createElement("th");
  const cellText = document.createTextNode("Simulator");
  cell.appendChild(cellText);
  row.appendChild(cell)
  const cell2 = document.createElement("th");
  const cellText2 = document.createTextNode("Description");
  cell2.appendChild(cellText2);
  row.appendChild(cell2)
   const cell3 = document.createElement("th");
  const cellText3 = document.createTextNode("Website");
  cell3.appendChild(cellText3);
  row.appendChild(cell3)
  tblHeader.appendChild(row);
  table.appendChild(tblHeader);
  
  tblbody = document.createElement("tbody");
  
  const numRows = frameworksMap.size;
  for(const [key, value] of frameworksMap) {
    const row = document.createElement("tr");
	const cell = document.createElement("td");
    const cellText = document.createTextNode(key);
    cell.appendChild(cellText);
	row.appendChild(cell)
	const cell2 = document.createElement("td");
    const cellText2 = document.createTextNode(value.description);
    cell2.appendChild(cellText2);
    row.appendChild(cell2)
	const cell3 = document.createElement("td");
    const cellText3 = document.createTextNode(value.url);
    cell3.appendChild(cellText3);
    row.appendChild(cell3)
	tblbody.appendChild(row);
  }	  
  table.appendChild(tblbody);
	
}
	

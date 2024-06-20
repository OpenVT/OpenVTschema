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
console.log("Hi " + selectionId);
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
	  const jsonURL = "/simulator_schemas/"+ jsonName;
	  await fetch(jsonURL)
		 .then((response) => response.json())
		 .then((json) => {
	   //console.log(json);
	 	  cachedData = json;
		  const newobjs = cachedData[typeStr];
		  for(const id in newobjs) {
		    //console.log(id+ ": "+ newobjs[id].name);
			if ( objectsMap.get(newobjs[id].name) == null) {// new object
			  objectsMap.set(newobjs[id].name,newobjs[id].description); 
			}
		  }
	  });
	
	}
	return objectsMap;
}

// returns Map of framework name and URL
async function getFrameworksThatSupport(supportedObjStr, objTypeStr) {
  const frameworksMap = new Map();
  for(let i= 0; i< frameworkNames.length; i++) {
	//const jsonName = "artistoo.json"
	  const jsonName = frameworkNames[i];
	  const jsonURL = "../simulator_schemas/"+ jsonName;
	  await fetch(jsonURL)
		 .then((response) => response.json())
		 .then((json) => {
	   //console.log(json);
	 	  frameworkData = json;
		  const newobjs = frameworkData[objTypeStr];
		  for(const id in newobjs) {
		    //console.log(id+ ": "+ newobjs[id].name);
			if ( newobjs[id].name === supportedObjStr) {
			  frameworksMap.set(frameworkData.name,frameworkData.description); 
			}
		  }
	  });
	
	}
	return frameworksMap;
	
}

async function fillOutTable(frameworksMap, objType) {
  let table;
  if ( objType.includes("object")) {
	table = document.getElementById(htmlObjTable)
  }
  else {
	table = document.getElementById(htmlProcessTable)
  }
 // DELETE OLd results first.
 // for(var i = 1;i<table.rows.length;){
 //   table.deleteRow(i);
 // }
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
    const cellText2 = document.createTextNode(value);
    cell2.appendChild(cellText2);
    row.appendChild(cell2)
	tblbody.appendChild(row);
  }	  
  table.appendChild(tblbody);
	
}
	


const framework_catagories = ["objects", "processes", "boundaries", "other info"] // Update as needed.

const frameworksdropdownMenuId = "framework_dropdown_menu"
const catagoryDropdownMenuId = "framework_catagories_dropdown_menu"
const catagories_divId = "framework_catagories_dropdown"
const editObjectDropdownMenuId = "edit_object_dropdown_menu"
const editObject_divId = "edit_object_dropdown"
const editForm_divId = "edit_schema_form_div"
const editForm_id = "edit_schema_form"
const viewSchema_btn = "framework_schema_view_btn"
const save_edits_divId = "saveEdits_div"
const save_edits_btnId = "saveEdits_btn"
const DROPDOWN_ITEM_CLASS = "dropdown-item"
const DROPDOWN_ITEM_ACTIVE_CLASS = "dropdown-item active"

window.onload = function (){
    document.getElementById(catagories_divId).style.visibility = "hidden";
    document.getElementById(editObject_divId).style.visibility = "hidden";
    document.getElementById(editForm_divId).style.visibility = "hidden";
    document.getElementById(save_edits_divId).style.visibility = "hidden";
    loadFrameworksDropdownMenu()
}



async function loadFrameworksDropdownMenu() 
{
    const dropDownList = document.getElementById(frameworksdropdownMenuId);
    for(let i = 0 ; i< frameworkNames.length + 1; i++)
    {
        let li = document.createElement("button")
        let frameworkNode = null
        li.className = DROPDOWN_ITEM_CLASS;
        if (i < frameworkNames.length) {
            li.id = "framework_" + i;
            frameworkNode = document.createTextNode(frameworkNames[i])
        }
        else {  // Add a new framework schema
            li.id = "framework_new";
            li.disabled = true;  // TODO Implement add new framework 
            frameworkNode = document.createTextNode("Add new framework")
        }
        li.appendChild(frameworkNode)
        li.addEventListener("click", (e) => {
            makeMenuItemActive(dropDownList, li);
            frameworkJsonCatagoryDropdownMenu(frameworkNode.nodeValue)
            });
        dropDownList.appendChild(li) 
    }
   
}

async function frameworkJsonCatagoryDropdownMenu(framework) {
    document.getElementById(catagories_divId).style.visibility = "visible";  
   // console.log("JsonCatagoryDrodownMenu selection: ", framework)
    setViewSchemaButtonEvent(framework)
    await clearDropDownMenu(catagoryDropdownMenuId);
    const dropDownList = document.getElementById(catagoryDropdownMenuId);
    for(let i = 0 ; i< framework_catagories.length; i++)
    {
        let li = document.createElement("button")
        let catagoryNode = null
        li.className = DROPDOWN_ITEM_CLASS;
        if (i < framework_catagories.length) {
            li.id = "catagory_" + i;
            catagoryNode = document.createTextNode(framework_catagories[i])
        }
        
        li.appendChild(catagoryNode)
        li.addEventListener("click", (e) => {
            //console.log("selection: ", catagoryNode.nodeValue);
            makeMenuItemActive(dropDownList, li);
            getCatagoryElements(framework, catagoryNode.nodeValue)
            });
        dropDownList.appendChild(li) 
    }

}


/*
  Return JSON of requested framework (processes, objects, boundries, etc ) from JSON file.
*/
async function getFramework_JSON(framework_jsonFileName_str) {
	console.log("JSon file name:  "+ framework_jsonFileName_str)	
	//const jsonName = "artistoo.json"
    let new_json = null
	  const jsonName = framework_jsonFileName_str;
	  const jsonURL = "simulator_schemas/"+ jsonName;
      try {
	    await fetch(jsonURL)
		     .then((response) => response.json())
		     .then((json) => {
	        //console.log(json);
		      new_json = json	  
	    });
      }
      catch(err) {
        window.alert(jsonURL + "not found" + err);
      }
	return new_json
}

async function getCatagoryElements(frameworkStr, catagoryStr){
    console.log(" getCatagoryElements: " + frameworkStr)
     
    let framework_JSON = await getFramework_JSON(frameworkStr)
    for (const key in framework_JSON) {
        if (key.localeCompare(catagoryStr) === 0) {
            editItemDropdownMenu(frameworkStr, framework_JSON, framework_JSON[catagoryStr], catagoryStr)
            return 1;
        }
        
    }

    if (catagoryStr.localeCompare(framework_catagories[3]) === 0) {  // Other info: get json 
        let other_JSON = new Map();
        for (const key in framework_JSON) {
            if((key.localeCompare(framework_catagories[0]) != 0) && (key.localeCompare(framework_catagories[1]) != 0)
             && (key.localeCompare(framework_catagories[2]) != 0) ) {
                other_JSON[key] = framework_JSON[key];
            }
        }
        editItemDropdownMenu(frameworkStr, framework_JSON, other_JSON, catagoryStr)
        return 1;
    }
    else {
        editItemDropdownMenu(frameworkStr, framework_JSON, null, catagoryStr)
        return 0; // Nothing returned
    }
    
}

async function editItemDropdownMenu(frameworkStr, framework_JSON, catagory_JSON, catagoryStr) {
    document.getElementById(editObject_divId).style.visibility = "visible";
    clearDropDownMenu(editObjectDropdownMenuId)
    const dropDownList = document.getElementById(editObjectDropdownMenuId);
    for(const key in catagory_JSON)
    {
        let li = document.createElement("button")
        let objectNode = null
        li.className = DROPDOWN_ITEM_CLASS;
        li.id = catagoryStr + "_" + key;
        if(catagory_JSON[key]["name"] == null) {
            objectNode = document.createTextNode(key)  // edit every sub element  
        }
        else {
            objectNode = document.createTextNode(catagory_JSON[key]["name"])
        }
        li.appendChild(objectNode)
        li.addEventListener("click", (e) => {
           console.log("Object value: ", objectNode.nodeValue)
           makeMenuItemActive(dropDownList, li);
           editFrameworkItem(frameworkStr, framework_JSON, objectNode.nodeValue, catagory_JSON[key])
            });
        dropDownList.appendChild(li) 
    }
        
    let li = document.createElement("button")
    let objectNode = null
    li.className = DROPDOWN_ITEM_CLASS;
    li.id = catagoryStr + "_new";
    li.disabled = true;  // TODO: implement add new item
    objectNode = document.createTextNode("New item")
    li.appendChild(objectNode)
    li.addEventListener("click", (e) => {
       console.log("Object value: ", objectNode.nodeValue)
       makeMenuItemActive(dropDownList, li);
       editFrameworkItem(frameworkStr, framework_JSON, objectNode.nodeValue, catagory_JSON.keys())
        });
    dropDownList.appendChild(li);

}

async function editFrameworkItem(frameworkStr, framework_JSON, item_JSON_key, catagoryJSON) {
    clearDropDownMenu(editForm_id)
    await elementVisible(editForm_divId);
    await elementVisible(save_edits_divId);
    setSaveEditsBtn_event(frameworkStr, framework_JSON, item_JSON_key, catagoryJSON);
    const editForm = document.getElementById(editForm_id);
    itemsToEdit = catagoryJSON;
    if( typeof catagoryJSON == "string") {  // then just single key:value 
        getSingleFormEntry(editForm, item_JSON_key, catagoryJSON)
    }
    else { await getFormEntries(editForm, itemsToEdit) }
   
}

// Returns a form entry consisting of a label and text input field
async function getFormEntries(form, itemsToEditDict) {
    for( let key in itemsToEditDict) {
            if( typeof itemsToEditDict[key] !== "string" && typeof itemsToEditDict[key] !== 'number') {
                const divElement = document.createElement('div');
                divElement.class = "mb-3";
                const labelElement = document.createElement('label');
                labelElement.class = "form-label";
                labelElement.textContent = key + ': ';
                labelElement.id = "outerKey_" + key;
                divElement.appendChild(labelElement);
                getFormEntries(divElement, itemsToEditDict[key])
                form.appendChild(divElement)
            }
            else {
                let value = itemsToEditDict[key]
                await getSingleFormEntry(form, key, value.toString())
            }
        
        }

}

async function getSingleFormEntry(form, key, valueStr) {
    const divElement = document.createElement('div');
    divElement.class = "mb-3";
    const labelElement = document.createElement('label');
    labelElement.class = "form-label"
    labelElement.textContent = key + ': ';
    labelElement.id = "key_" + key;
    
    const inputElement = document.createElement('input');
    inputElement.class = "form-control"
    inputElement.type = 'text';
    inputElement.maxlength = 1000;
    inputElement.style.width = "50%"
    inputElement.value = valueStr;
    inputElement.id = "valueFor_" + key;
    if(key.includes("_id")) {
        inputElement.disabled = true;
    }
    inputElement.name = "input_" + valueStr.toLowerCase();
    divElement.appendChild(labelElement);
    divElement.appendChild(inputElement);
    form.appendChild(divElement)
}

async function makeMenuItemActive(active_dropDownList, active_element) {
    const children = active_dropDownList.children;
    for(let j = 0; j< children.length; j++) {
        let child = children[j];
        if ( child.id === active_element.id ) {
            child.className = DROPDOWN_ITEM_ACTIVE_CLASS;
        }
        else {
            child.className = DROPDOWN_ITEM_CLASS;
        }
    }
}

async function elementVisible(elementId) {
    document.getElementById(elementId).style.visibility = "visible";
}

async function elementHide(elementId) {
    document.getElementById(elementId).style.visibility = "hidden";
}

async function setViewSchemaButtonEvent(schemaFileName) {
    schema_btn = document.getElementById(viewSchema_btn)
    schema_btn.addEventListener("click", (e) => {
        //console.log("string value: ${schemaFileName}")
        viewSchemaInAnotherPage(schemaFileName)
         });
}

async function setSaveEditsBtn_event(frameworkFileName, framework_JSON, item_JSON_key, catagoryJSON){
    saveEdits = document.getElementById(save_edits_btnId);
    saveEdits.addEventListener("click", (e) => {
        saveSchemaEdits(frameworkFileName, framework_JSON, item_JSON_key, catagoryJSON)
    });
}

async function saveSchemaEdits(frameworkFileName, framework_JSON, item_key, itemEditJSON) {
    console.log("In saveSchemaEdits()");
    // need to insert edits into JSON here...
    const newJSON = createNewJSON(framework_JSON, item_key, itemEditJSON);
    saveSchemaToFile(frameworkFileName, framework_JSON);

}

async function viewSchemaInAnotherPage(frameworkFileName) {
    urlStr = "viewSchema.html?schema_fileName=simulator_schemas/" + frameworkFileName  
    window.open(urlStr, '_blank').focus();
}

async function createNewJSON(framework_JSON, item_key, itemToEditJSON) {
    const isInteger = (string) => string == Number.parseInt(string)
    let newItemJSON = {}
    let subItems = {}
    let arrayKeyVals = false
    let keyWithSubArray = "";
    let form_lbls = document.querySelectorAll("label");
    let form_inputs = document.querySelectorAll("input");
    for(let i= 0; i< form_lbls.length; i++) {  
        let keyEle = form_lbls[i];
        let valueEle = form_inputs[i];
        let key = keyEle.innerText.replace(":","");
        if(keyEle.id.includes("outerKey_")) { // value holds an Array of key value pairs
            arrayKeyVals = true;
            keyWithSubArray = key;
        }
        else {
            let newValue = valueEle.value;
            if(isInteger(key)) {
                subItems[key] = newValue;
            } 
            else { 
                if(arrayKeyVals) {  // reset array subset
                    arrayKeyVals = false;
                    newIteJSON[keyWithSubArray] = subItems;
                    keyWithSubArray = ""
                    subItems = {};
                }
                else {
                    newItemJSON[key] = newValue;
                }
            }
              
        }
        console.log("Endd...");
    }
}

function saveSchemaToFile(fileName, json_str) {
    const fileExt = ".json";
    const file_name = "copy_" + fileName;
    var promptFilename;
         
    if ((promptFilename = prompt("Save file as (" + fileExt + ") ", file_name))) {
        var textBlob = new Blob([JSON.stringify(json_str, null, 2)], {
          type: "text/plain",
        });
        var downloadLink = document.createElement("a");
        
        if( promptFilename.includes(fileExt) || promptFilename.includes(".json") ) {
            downloadLink.download = promptFilename; }
        else { downloadLink.download = promptFilename + fileExt; }
     
        downloadLink.innerHTML = "Download File";
        downloadLink.href = window.URL.createObjectURL(textBlob);
        downloadLink.click();
    }
  }

async function clearDropDownMenu(dropDownId) {
    document.getElementById(dropDownId).innerHTML =
                    null;

}
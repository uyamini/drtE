// Code from https://www.aspsnippets.com/Articles/Import-CSV-File-to-HTML-Table-using-JavaScript.aspx


function Upload() {
    var fileUpload = document.getElementById("fileUpload");
    var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv|.txt)$/;
    if (regex.test(fileUpload.value.toLowerCase())) {
        if (typeof (FileReader) != "undefined") {
            var reader = new FileReader();
            reader.onload = function (e) {
                var table = document.createElement("table");
                // table.style.cellspacing="20px";
                var rows = e.target.result.split("\n");
                for (var i = 0; i < rows.length; i++) {
                    var cells = rows[i].split(",");
                    if (cells.length > 1) {
                        var row = table.insertRow(-1);
                        for (var j = 0; j < cells.length; j++) {
                            var cell = row.insertCell(-1);
                            cell.innerHTML = cells[j];
                        }
                    }
                }
                var dvCSV = document.getElementById("dvCSV");
                dvCSV.innerHTML = "";
                dvCSV.appendChild(table);
            }
            reader.readAsText(fileUpload.files[0]);
        } else {
            alert("This browser does not support HTML5.");
        }
    } else {
        alert("Please upload a valid CSV file.");
    }
}

function RetrieveConfigCheckboxes() {
    const form = document.querySelector('form');
    form.addEventListener('submit', e => {
        e.preventDefault();

    const values = Array.from(document.querySelectorAll('input[type=checkbox]:checked'))
        .map(item => item.value)
        .join(','); 
    });

    //Making a separate folder: 
    const fs = require('fs')
    const folderName = '/config'
    try {
        if (!fs.existsSync(folderName)) {
        fs.mkdirSync(folderName)}
    }   catch (err) {
        console.error(err)
    }
    //Writing the variable values to a separate file in the folder config
    fs.writeFile('/config/config.txt', values, err => {
        if (err) {
          console.error(err)
          return
        }
        //file written successfully
      })
}

const showPostDetail = ev => {
    const html = `
            <div class ="modal-bg">
                <div class ="modal">
                    We are cleaning your data!
                </div>    
            </div>`;
    document.querySelector('#modal-container').innerHTML = html;
    console.log('This function was called')
};

const CloseModal = ev => {
    const html = '';
    document.querySelector('#modal-container').innerHTML = html;
};
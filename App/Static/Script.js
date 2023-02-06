function checkFileType(event) {
	event.preventDefault();
	let file = document.getElementById("file").files[0];
	if (!!file) {
		console.log(file);
		console.log(file.name);
		let extension = file.name.split(".")[file.name.split(".").length - 1];
		console.log(extension);
		if (
			extension.toLowerCase() == "pdf"
		) {
            window.alert("File Type Accepted")
		}else{
            alert("File Type is not accepted")
            document.getElementById("file").value=null;
        }
	}
}



let TransctionData=[]

async function getTableData(event) {
	try {
		let response =await fetch('/get_transactions',{
			method:"POST"
		})
		let result=await response.json()
		console.log(result);
		TransctionData=result.data
	} catch (error) {
		console.log(error);
	}
}
getTableData()
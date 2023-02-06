function checkFileType(event) {
	event.preventDefault();
	let file = document.getElementById("file").files[0];
	if (!!file) {
		let extension = file.name.split(".")[file.name.split(".").length - 1];
		if (extension.toLowerCase() == "pdf") {
			window.alert("File Type Accepted");
		} else {
			alert("File Type is not accepted");
			document.getElementById("file").value = null;
		}
	}
}

let TransactionData = {};

async function getTableData(event) {
	try {
		let response = await fetch("/get_transactions", {
			method: "POST",
		});
		let result = await response.json();
		TransactionData = result;
		getGraphData();
	} catch (error) {
		console.log(error);
	}
}
getTableData();

async function getGraphData() {
	try {
		let response = await fetch("/get_cumulative_data", {
			method: "POST",
		});
		let result = await response.json();
		let cumulative_balance_graph = document.getElementById("cumulative_balance_graph");
		let chart = new Chart(cumulative_balance_graph, {
			type: "line",
			data: {
				labels: result.x,
				datasets: [
					{
						label: "Balance",
						data: result.y,
						borderWidth: 1,
					},
				],
			},
			options: {
				scales: {
					y: {
						beginAtZero: true,
					},
				},
			},
		});
	} catch (error) {
		console.log(error);
	}
}

function getData() {
	let matcher = document.getElementById("search").value.toLowerCase();
	let counter = 0;
	if (matcher != "") {
		let html_content = `
    <table border="1">
    <thead>
        <tr>
            <th>Transaction Date</th>
            <th>Description by Bank</th>
            <th>Amount</th>
            <th>Payment Mode</th>
            <th>Recipient Name</th>
            <th>Transaction Type</th>
        </tr>
    </thead>
    <tbody>
    `;
		for (
			let index = 0;
			index < Object.keys(TransactionData["Date"]).length;
			index++
		) {
			if (
				String(TransactionData["Date"][index])
					.toLocaleLowerCase()
					.indexOf(matcher) != -1 ||
				String(TransactionData["Description"][index])
					.toLocaleLowerCase()
					.indexOf(matcher) != -1 ||
				String(TransactionData["Amount"][index])
					.toLocaleLowerCase()
					.indexOf(matcher) != -1 ||
				String(TransactionData["Payment_Mode"][index])
					.toLocaleLowerCase()
					.indexOf(matcher) != -1 ||
				String(TransactionData["Recipient_Name"][index])
					.toLocaleLowerCase()
					.indexOf(matcher) != -1
			) {
				counter +=1;
				html_content += `
            <tr>
            <td>${TransactionData["Date"][index]}</td>
            <td>${TransactionData["Description"][index]}</td>
            <td>${TransactionData["Amount"][index]}</td>
            <td>${TransactionData["Payment_Mode"][index]}</td>
            <td>${TransactionData["Recipient_Name"][index]}</td>
            <td>${TransactionData["Type"][index]}</td>
            </tr>
            `;
				counter++;
			}
		}
		html_content += `
        </tbody>
    </table>
    `;
		if (counter > 0) {
			window.alert(counter + " Rows Found");
			document.getElementById("outputTransactions").innerHTML =
				html_content;
		} else document.getElementById("outputTransactions").innerHTML = "";
	}
}

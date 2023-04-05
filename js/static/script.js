function pass_to_python() {
    var input = document.getElementById("input").value;
    console.log(input); // Print the input value to the console

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/recommend_songs");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Parse the response data as a JavaScript object
            var response = JSON.parse(xhr.responseText);
            console.log(response);
            // Update the contents of an HTML element with the processed data
            document.getElementById("result").innerHTML = response.processed_data;
        }
    };

    xhr.send(JSON.stringify({"input":input}));
}

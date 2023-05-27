document.getElementById('markButton').onclick = function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let input_text = document.getElementById('myText');

        if (!input_text.value.trim()) {
            alert('Please enter text in the input box');
            return;
        }

        let url = tabs[0].url;  // Get the URL of the current tab
        console.log("OOGA");

        // Send the URL to the server
        fetch('http://localhost:3000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({url: url, text: input_text.value})
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            chrome.tabs.sendMessage(tabs[0].id, {command: "markVideo", timestamps: data.timestamps});
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
};
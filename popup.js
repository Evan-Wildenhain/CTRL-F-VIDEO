document.addEventListener('DOMContentLoaded', (event) => {
    chrome.runtime.sendMessage({action: "getGlobalData"}, function(response) {
        let globalData = response.data;

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            let currentTabUrl = tabs[0].url;
            let bgPageUrl = globalData.url;
            if (currentTabUrl === bgPageUrl) {
                let previousText = globalData.inputText;
                document.getElementById('myText').value = previousText;
            }
        });
    });
});



chrome.runtime.sendMessage({action: "getGlobalData"}, function(response) {
    let globalData = response.data;
    return globalData
});


document.getElementById('markButton').onclick = function() {
    chrome.runtime.sendMessage({action: "getGlobalData"}, function(response) {
        let globalData = response.data;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs)
        {
            let currentTablUrl = tabs[0].url;
            let bgPageUrl = globalData.url;
            let input_text = document.getElementById('myText');
            if (currentTablUrl === bgPageUrl && input_text.value == globalData.inputText){
                chrome.tabs.sendMessage(tabs[0].id,
                    {command: "markVideo",
                        timestamps: globalData.responseData.timestamps,
                        extended_timestamps: globalData.responseData.extended_timestamps,
                        identical_phoneme_timestamps: globalData.responseData.phoneme_matches,
                        similar_phoneme_timestamps: globalData.responseData.similar_phonemes
                    })
            }
            else {
                processVideo('markVideo');
            }
        })
    });
};


document.getElementById('RemoveButton').onclick = function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {command: "removeMarkers"});
    });
};

document.getElementById('similarButton').onclick = function() {
    chrome.runtime.sendMessage({action: "getGlobalData"}, function(response) {
        let globalData = response.data;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, 
                {command: "showSimilar",
                    timestamps: globalData.responseData.timestamps,
                    extended_timestamps: globalData.responseData.extended_timestamps,
                    identical_phoneme_timestamps: globalData.responseData.phoneme_matches,
                    similar_phoneme_timestamps: globalData.responseData.similar_phonemes
                }
            );
        });
    });
};

document.getElementById('allButton').onclick = function() {
    chrome.runtime.sendMessage({action: "getGlobalData"}, function(response) {
        let globalData = response.data;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, 
                {command: "showAll",
                    timestamps: globalData.responseData.timestamps,
                    extended_timestamps: globalData.responseData.extended_timestamps,
                    identical_phoneme_timestamps: globalData.responseData.phoneme_matches,
                    similar_phoneme_timestamps: globalData.responseData.similar_phonemes
                }
            );
        });
    });
};

function processVideo(command) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let input_text = document.getElementById('myText');

        if (!input_text.value.trim()) {
            alert('Please enter text in the input box');
            return;
        }

        let url = tabs[0].url;  // Get the URL of the current tab

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
            
            chrome.runtime.sendMessage({
                action: "setGlobalData",
                data: {inputText: input_text.value, responseData: data, url: tabs[0].url}
            }, response => {
                console.log(response.status);
            });

            chrome.tabs.sendMessage(tabs[0].id, 
                {command: command,
                     timestamps: data.timestamps,
                      extended_timestamps: data.extended_timestamps,
                       identical_phoneme_timestamps: data.phoneme_matches,
                        similar_phoneme_timestamps: data.similar_phonemes});
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
}

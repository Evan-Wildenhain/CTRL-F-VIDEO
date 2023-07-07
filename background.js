let globalInfo = {
    inputText: "",
    url: "",
    responseData: {}
};


// Listen for messages from the popup script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getGlobalData") {
        // Return the current global data
        sendResponse({data: globalInfo});
    } else if (request.action === "setGlobalData") {
        // Update the global data with the data from the message
        globalInfo.inputText = request.data.inputText;
        globalInfo.responseData = request.data.responseData;
        globalInfo.url = request.data.url;
        sendResponse({status: "success"});
    }
    return true;
});
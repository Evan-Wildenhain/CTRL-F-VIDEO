let markersShown = false;  // State to track whether markers are shown or hidden

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.command === "markVideo") {
        hideMarkers();
        showMarkers(request.timestamps, "#57DD73");
        showMarkers(request.extended_timestamps, "#1EEAFF");

        // Toggle the state
        markersShown = true;
        console.log("done showing")
    } else if (request.command === "removeMarkers") {
        hideMarkers();
        markersShown = false;
    }
    else if (request.command === "showSimilar") {
        hideMarkers();
        showMarkers(request.identical_phoneme_timestamps, "#FF9600");
        showMarkers(request.similar_phoneme_timestamps, "#D81EFF");
        console.log("here");
        markersShown = true;
    }
    else if (request.command === "showAll") {
        hideMarkers();
        showMarkers(request.timestamps, "#57DD73");
        showMarkers(request.extended_timestamps, "#1EEAFF");
        showMarkers(request.identical_phoneme_timestamps, "#FF9600");
        showMarkers(request.similar_phoneme_timestamps, "#D81EFF");
        console.log("HERE");
        markersShown = true;
    }
});


function hideMarkers() {
    // If markers are currently shown, hide them
    let markers = document.querySelectorAll('.marker');
    markers.forEach(function(marker) {
        marker.style.display = 'none';
    });
}

function showMarkers(timestamps, color) {
    // If markers are currently hidden, show them
    let videoElement = document.querySelector("video");
    let progressBar = document.querySelector('.ytp-progress-bar');

    let videoDuration = videoElement.duration;
    if (!Array.isArray(timestamps) || !timestamps.length) {
        console.log("no times")
        return
    }
    timestamps.forEach(function(timestamp) {
        let position = (timestamp / videoDuration)* 100;
        // Create the marker
        let marker = document.createElement('div');
        marker.className = 'marker';  // Add a class to the marker for easy selection
        marker.style.position = 'absolute';
        marker.style.height = '100%';
        marker.style.width = '2px';
        marker.style.backgroundColor = color;
        marker.style.left = `${position}%`;

        // Append the marker to the progress bar
        progressBar.appendChild(marker);
    });
}

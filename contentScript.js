let markersShown = false;  // State to track whether markers are shown or hidden

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.command === "markVideo") {
        if (markersShown) {
            // If markers are currently shown, hide them
            let markers = document.querySelectorAll('.marker');
            markers.forEach(function(marker) {
                marker.style.display = 'none';
            });
        } else {
            // If markers are currently hidden, show them
            let videoElement = document.querySelector("video");
            let progressBar = document.querySelector('.ytp-progress-bar');

            let videoDuration = videoElement.duration;
            request.timestamps.forEach(function(timestamp) {

                let position = (timestamp / videoDuration)* 100;
                // Create the marker
                let marker = document.createElement('div');
                marker.className = 'marker';  // Add a class to the marker for easy selection
                marker.style.position = 'absolute';
                marker.style.height = '100%';
                marker.style.width = '2px';
                marker.style.backgroundColor = 'red';
                marker.style.left = `${position}%`;

                // Append the marker to the progress bar
                progressBar.appendChild(marker);
        });
        }

        // Toggle the state
        markersShown = !markersShown;
    }
});
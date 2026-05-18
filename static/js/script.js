function startSystem() {
    document.getElementById("start-text").innerHTML = 'Sistemul rulează...';
    
    document.getElementById("video-feed").src = "http://127.0.0.1:5000/video_feed";
}
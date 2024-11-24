document.addEventListener('DOMContentLoaded', () => {
    const videoList = document.getElementById('videoList');
    const videos = Array.from(videoList.getElementsByClassName('video-card'));

    function playVideo(relativePath, name, index) {
        const videoPlayer = document.createElement('video');
        videoPlayer.src = `/videos/${relativePath}`;
        videoPlayer.controls = true;
        videoPlayer.style.maxWidth = '80%';
        videoPlayer.style.maxHeight = '450px';
        videoPlayer.autoplay = true;

        const playerModal = document.createElement('div');
        playerModal.style.position = 'fixed';
        playerModal.style.top = '0';
        playerModal.style.left = '0';
        playerModal.style.width = '100%';
        playerModal.style.height = '100%';
        playerModal.style.backgroundColor = 'rgba(0,0,0,0.8)';
        playerModal.style.display = 'flex';
        playerModal.style.justifyContent = 'center';
        playerModal.style.alignItems = 'center';
        playerModal.style.zIndex = '1000';

        const prevButton = document.createElement('button');
        prevButton.textContent = '←';
        prevButton.style.position = 'absolute';
        prevButton.style.left = '20px';
        prevButton.style.top = '50%';
        prevButton.style.transform = 'translateY(-50%)';
        prevButton.style.fontSize = '24px';
        prevButton.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        prevButton.style.color = 'white';
        prevButton.style.border = 'none';
        prevButton.style.padding = '10px';
        prevButton.style.cursor = 'pointer';

        const nextButton = document.createElement('button');
        nextButton.textContent = '→';
        nextButton.style.position = 'absolute';
        nextButton.style.right = '20px';
        nextButton.style.top = '50%';
        nextButton.style.transform = 'translateY(-50%)';
        nextButton.style.fontSize = '24px';
        nextButton.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        nextButton.style.color = 'white';
        nextButton.style.border = 'none';
        nextButton.style.padding = '10px';
        nextButton.style.cursor = 'pointer';

        nextButton.addEventListener('click', () => {
            if (index < videos.length - 1) {
                const nextVideo = videos[index + 1].dataset.filename;
                document.body.removeChild(playerModal);
                playVideo(nextVideo, nextVideo, index + 1);
            }
        });

        prevButton.addEventListener('click', () => {
            if (index > 0) {
                const prevVideo = videos[index - 1].dataset.filename;
                document.body.removeChild(playerModal);
                playVideo(prevVideo, prevVideo, index - 1);
            }
        });

        playerModal.appendChild(videoPlayer);
        playerModal.appendChild(prevButton);
        playerModal.appendChild(nextButton);
        document.body.appendChild(playerModal);

        videoPlayer.load();
        videoPlayer.play().catch(error => {
            console.error("Erro ao tentar reproduzir o vídeo:", error);
        });

        playerModal.addEventListener('click', (event) => {
            if (event.target === playerModal) {
                document.body.removeChild(playerModal);
            }
        });
    }

    videos.forEach((videoCard, index) => {
        const videoFile = videoCard.dataset.filename;
        videoCard.addEventListener('click', () => playVideo(videoFile, videoFile, index));
    });    
});

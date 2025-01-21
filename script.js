// script.js
// This script will be executed after the DOM has been loaded
// and the mediaArray has been defined in the HTML file.

document.addEventListener("DOMContentLoaded", () => {
  const mediaArray = [
      // Media objects...
  ];

  const galleryContainer = document.querySelector('.gallery');

  // Sort media by aspect ratio (landscape, portrait, square)
  const sortedMedia = mediaArray.sort((a, b) => {
      const aRatio = a.streams[0].width / a.streams[0].height;
      const bRatio = b.streams[0].width / b.streams[0].height;
      return bRatio - aRatio; // Descending order by width/height ratio
  });

  sortedMedia.forEach(item => {
      // Create a wrapper div
      const galleryItem = document.createElement('div');
      galleryItem.classList.add('gallery-item');

      // Determine media aspect ratio
      const { width, height } = item.streams[0];
      if (width > height) {
          galleryItem.classList.add('landscape');
      } else if (width < height) {
          galleryItem.classList.add('portrait');
      } else {
          galleryItem.classList.add('square');
      }

      // Check if it's an image or video
      if (item.mime_type.startsWith('image')) {
          const img = document.createElement('img');
          img.src = item.file_path;
          img.alt = 'Gallery Item';
          galleryItem.appendChild(img);
      } else if (item.mime_type.startsWith('video')) {
          const video = document.createElement('video');
          video.controls = true;
          const source = document.createElement('source');
          source.src = item.file_path;
          source.type = item.mime_type;
          video.appendChild(source);
          galleryItem.appendChild(video);
      }

      // Add the gallery item to the container
      galleryContainer.appendChild(galleryItem);
  });
});

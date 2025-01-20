// script.js
document.addEventListener("DOMContentLoaded", () => {
    const mediaArray = [
      // Your image/video objects ...
    ];
    
    const galleryContainer = document.querySelector('.gallery');
  
    mediaArray.forEach(item => {
      // Create a wrapper div
      const galleryItem = document.createElement('div');
      galleryItem.classList.add('gallery-item');
      
      // Check if it's an image or video by mime_type
      if (item.mime_type.startsWith('image')) {
        const img = document.createElement('img');
        img.src = item.file_path;
        img.alt = 'Gallery Item';
        if (item.width > item.height) {
          img.classList.add('landscape');
        }
        galleryItem.appendChild(img);
      } else if (item.mime_type.startsWith('video')) {
        const video = document.createElement('video');
        video.controls = true;
        const source = document.createElement('source');
        source.src = item.file_path;
        source.type = item.mime_type;
        if (item.height > item.width) {
          video.classList.add('portrait');
        }
        video.appendChild(source);
        galleryItem.appendChild(video);
      }
      
      // Add to the gallery
      galleryContainer.appendChild(galleryItem);
    });
  });
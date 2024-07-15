// frontend/script.js
function uploadImage() {
    const input = document.getElementById('imageUpload');
    if (input.files && input.files[0]) {
        const formData = new FormData();
        formData.append('file', input.files[0]);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.filepath) {
                runDetection(data.filepath);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function runDetection(imagePath) {
    fetch('/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_path: imagePath })
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
        runDepthEstimation(imagePath);
    })
    .catch(error => console.error('Error:', error));
}

function runDepthEstimation(imagePath) {
    fetch('/estimate_depth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_path: imagePath })
    })
    .then(response => response.json())
    .then(data => {
        displayDepthMap(data.depth_map);
    })
    .catch(error => console.error('Error:', error));
}

function displayResults(detections) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    const img = document.createElement('img');
    img.src = detections.image_path;
    resultsDiv.appendChild(img);

    detections.forEach(detection => {
        const div = document.createElement('div');
        div.innerHTML = `Class: ${detection.class} | Confidence: ${detection.confidence}`;
        resultsDiv.appendChild(div);
    });
}

function displayDepthMap(depthMap) {
    const resultsDiv = document.getElementById('results');
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    const width = depthMap[0].length;
    const height = depthMap.length;
    canvas.width = width;
    canvas.height = height;

    const imgData = ctx.createImageData(width, height);
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const value = Math.floor(depthMap[y][x] * 255);
            const index = (y * width + x) * 4;
            imgData.data[index] = value;
            imgData.data[index + 1] = value;
            imgData.data[index + 2] = value;
            imgData.data[index + 3] = 255;
        }
    }

    ctx.putImageData(imgData, 0, 0);
    resultsDiv.appendChild(canvas);
}

async function initPoseEstimation() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('output');
    const ctx = canvas.getContext('2d');
  
    // Function to set up the camera
    async function setupCamera() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 },
            audio: false
          });
          video.srcObject = stream;
          return new Promise((resolve) => {
            video.onloadedmetadata = () => {
              resolve(video);
            };
          });
        } catch (err) {
          alert("Error accessing the camera: " + err);
        }
      } else {
        alert("Camera not available.");
      }
    }
  
    // Load the PoseNet model
    const net = await posenet.load();
  
    await setupCamera();
    video.play();
  
    // Function to continuously detect the pose and evaluate it
    async function detectPose() {
      const pose = await net.estimateSinglePose(video, { flipHorizontal: false });
      
      // Clear canvas and draw the video frame.
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // Draw keypoints on the canvas
      drawKeypoints(pose.keypoints, 0.5, ctx);
  
      // Evaluate the pose
      let message = evaluatePose(pose);
      ctx.font = "20px Arial";
      ctx.fillStyle = "blue";
      ctx.fillText(message, 10, 30);
      
      requestAnimationFrame(detectPose);
    }
  
    detectPose();
  }
  
  // Utility function to draw keypoints
  function drawKeypoints(keypoints, minConfidence, ctx, scale = 1) {
    keypoints.forEach(keypoint => {
      if (keypoint.score < minConfidence) return;
      const { y, x } = keypoint.position;
      ctx.beginPath();
      ctx.arc(x * scale, y * scale, 5, 0, 2 * Math.PI);
      ctx.fillStyle = "aqua";
      ctx.fill();
    });
  }
  
  // Basic evaluation function based on overall pose score
  function evaluatePose(pose) {
    // You can add more detailed checks here (e.g., specific joint angles)
    if (pose.score > 0.8) {
      return "Great job! Your form looks correct.";
    } else if (pose.score > 0.5) {
      return "You're doing okay, but try to improve your posture.";
    } else {
      return "Your pose is off. Please adjust your posture.";
    }
  }
  
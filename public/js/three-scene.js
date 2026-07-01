(function() {
  try {
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0a0e1a, 0.0008);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 30;

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: "low-power"
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.getElementById('three-container').appendChild(renderer.domElement);

    const particlesGeo = new THREE.BufferGeometry();
    const particleCount = 1200;
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);
    const velocities = [];

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 100;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 80;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 60;

      const colorChoice = Math.random();
      if (colorChoice < 0.33) {
        colors[i * 3] = 0.4; colors[i * 3 + 1] = 0.49; colors[i * 3 + 2] = 0.92;
      } else if (colorChoice < 0.66) {
        colors[i * 3] = 0.22; colors[i * 3 + 1] = 0.74; colors[i * 3 + 2] = 0.97;
      } else {
        colors[i * 3] = 0.46; colors[i * 3 + 1] = 0.29; colors[i * 3 + 2] = 0.64;
      }

      sizes[i] = Math.random() * 2 + 0.5;
      velocities.push({
        x: (Math.random() - 0.5) * 0.02,
        y: (Math.random() - 0.5) * 0.02,
        z: (Math.random() - 0.5) * 0.02
      });
    }

    particlesGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particlesGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    particlesGeo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const particleTexture = (() => {
      const canvas = document.createElement('canvas');
      canvas.width = 16; canvas.height = 16;
      const ctx = canvas.getContext('2d');
      const gradient = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
      gradient.addColorStop(0, 'rgba(255,255,255,1)');
      gradient.addColorStop(0.3, 'rgba(255,255,255,0.8)');
      gradient.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 16, 16);
      return new THREE.CanvasTexture(canvas);
    })();

    const particleMat = new THREE.PointsMaterial({
      size: 0.4,
      map: particleTexture,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      vertexColors: true,
      opacity: 0.8
    });

    const particleSystem = new THREE.Points(particlesGeo, particleMat);
    scene.add(particleSystem);

    const connectGeo = new THREE.BufferGeometry();
    const connectPositions = new Float32Array(particleCount * 3);
    const connectIndices = [];
    const color = new THREE.Color();
    const linePositions = [];

    for (let i = 0; i < particleCount * 3; i++) {
      connectPositions[i] = positions[i];
    }

    function updateConnections() {
      linePositions.length = 0;
      for (let i = 0; i < particleCount; i++) {
        for (let j = i + 1; j < particleCount; j++) {
          const dx = positions[i * 3] - positions[j * 3];
          const dy = positions[i * 3 + 1] - positions[j * 3 + 1];
          const dz = positions[i * 3 + 2] - positions[j * 3 + 2];
          const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
          if (dist < 8) {
            linePositions.push(positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2]);
            linePositions.push(positions[j * 3], positions[j * 3 + 1], positions[j * 3 + 2]);
          }
        }
      }

      const lineGeo = new THREE.BufferGeometry();
      lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
      const lineMat = new THREE.LineBasicMaterial({
        color: 0x667eea,
        transparent: true,
        opacity: 0.06
      });
      if (window._lineSystem) {
        scene.remove(window._lineSystem);
        window._lineSystem.geometry.dispose();
        window._lineSystem.material.dispose();
      }
      window._lineSystem = new THREE.LineSegments(lineGeo, lineMat);
      scene.add(window._lineSystem);
    }

    updateConnections();

    let mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', (e) => {
      mouseX = (e.clientX / window.innerWidth) * 2 - 1;
      mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    function animate() {
      requestAnimationFrame(animate);
      const pos = particleSystem.geometry.attributes.position.array;
      for (let i = 0; i < particleCount; i++) {
        pos[i * 3] += velocities[i].x;
        pos[i * 3 + 1] += velocities[i].y;
        pos[i * 3 + 2] += velocities[i].z;
        if (Math.abs(pos[i * 3]) > 50) velocities[i].x *= -1;
        if (Math.abs(pos[i * 3 + 1]) > 40) velocities[i].y *= -1;
        if (Math.abs(pos[i * 3 + 2]) > 30) velocities[i].z *= -1;
      }
      particleSystem.geometry.attributes.position.needsUpdate = true;

      if (window._lineSystem) {
        const linePos = window._lineSystem.geometry.attributes.position.array;
        let idx = 0;
        for (let i = 0; i < particleCount && idx < linePos.length; i++) {
          for (let j = i + 1; j < particleCount && idx < linePos.length; j++) {
            const dx = pos[i * 3] - pos[j * 3];
            const dy = pos[i * 3 + 1] - pos[j * 3 + 1];
            const dz = pos[i * 3 + 2] - pos[j * 3 + 2];
            const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
            if (dist < 8 && idx + 5 < linePos.length) {
              linePos[idx] = pos[i * 3];
              linePos[idx + 1] = pos[i * 3 + 1];
              linePos[idx + 2] = pos[i * 3 + 2];
              linePos[idx + 3] = pos[j * 3];
              linePos[idx + 4] = pos[j * 3 + 1];
              linePos[idx + 5] = pos[j * 3 + 2];
              idx += 6;
            }
          }
        }
        window._lineSystem.geometry.attributes.position.needsUpdate = true;
        window._lineSystem.geometry.setDrawRange(0, idx);
      }

      particleSystem.rotation.x += 0.0001;
      particleSystem.rotation.y += 0.0002;
      particleSystem.rotation.x += (mouseY * 0.005 - particleSystem.rotation.x) * 0.01;
      particleSystem.rotation.y += (mouseX * 0.005 - particleSystem.rotation.y) * 0.01;

      renderer.render(scene, camera);
    }

    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    window.__threeReady = true;
  } catch (e) {
    console.warn('Three.js scene skipped:', e.message);
  }
})();

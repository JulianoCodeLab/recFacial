const startCameraBtn = document.getElementById("startCameraBtn");
const stopCameraBtn = document.getElementById("stopCameraBtn");
const captureBtn = document.getElementById("captureBtn");
const cameraModal = document.getElementById("cameraModal");
const video = document.getElementById("cameraPreview");

let stream = null;

// Abrir a câmera
startCameraBtn.addEventListener("click", async () => {
  try {
    cameraModal.setAttribute("aria-hidden", "false");

    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    await video.play();

  } catch (err) {
    console.error("Erro ao acessar a câmera:", err);
    alert("Erro ao acessar a câmera. Permita o uso da câmera.");
    cameraModal.setAttribute("aria-hidden", "true");
  }
});

// Fechar câmera
stopCameraBtn.addEventListener("click", () => {
  fecharCamera();
});

function fecharCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
  video.srcObject = null;
  cameraModal.setAttribute("aria-hidden", "true");
}

// Capturar imagem + enviar para o servidor
captureBtn.addEventListener("click", async () => {
  if (!stream) return alert("Câmera não iniciada.");

  // Captura o frame como imagem
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imagemBase64 = canvas.toDataURL("image/png");

  // Pegar os dados do formulário (corrigido!)
  const nome = document.getElementById("nomeCadastro").value.trim();
  const curso = document.getElementById("curso").value.trim();
  const periodo = document.getElementById("periodo").value.trim();

  if (!nome || !curso || !periodo) {
    return alert("Preencha todos os campos!");
  }

  // Enviar para API
  try {
    const resposta = await fetch("http://localhost:5000/cadastrar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nome: nome,
        curso: curso,
        periodo: periodo,
        imagem: imagemBase64
      })
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
      alert("❌ Erro: " + dados.erro);
      return;
    }

   alert("✅ Cadastro realizado com sucesso!");
fecharCamera();


  } catch (err) {
    console.error(err);
    alert("Erro ao enviar dados para o servidor.");
  }
});
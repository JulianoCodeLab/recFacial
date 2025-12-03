const startCameraBtn = document.getElementById("startCameraBtn");
const stopCameraBtn = document.getElementById("stopCameraBtn");
const captureBtn = document.getElementById("captureBtn");
const cameraModal = document.getElementById("cameraModal");
const video = document.getElementById("cameraPreview");

const permissionModal = document.getElementById("permissionModal");
const allowBtn = document.getElementById("allowBtn");
const denyBtn = document.getElementById("denyBtn");

let stream = null;

// ==========================
// 1. ABRIR MODAL DE PERMISSÃO
// ==========================
startCameraBtn.addEventListener("click", () => {
  permissionModal.setAttribute("aria-hidden", "false");
});

// Se o usuário ACEITA
allowBtn.addEventListener("click", async () => {
  permissionModal.setAttribute("aria-hidden", "true");
  abrirCamera();
});

// Se o usuário NEGA
denyBtn.addEventListener("click", () => {
  permissionModal.setAttribute("aria-hidden", "true");
  alert("Você precisa permitir o uso da imagem para continuar.");
});

// ==========================
// 2. FUNÇÃO PARA ABRIR CÂMERA
// ==========================
async function abrirCamera() {
  try {
    cameraModal.setAttribute("aria-hidden", "false");

    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    await video.play();
  } catch (err) {
    console.error("Erro ao acessar câmera:", err);
    alert("Erro ao acessar a câmera. Permita o uso da câmera.");
    cameraModal.setAttribute("aria-hidden", "true");
  }
}

// ==========================
// 3. FECHAR CÂMERA
// ==========================
stopCameraBtn.addEventListener("click", () => {
  fecharCamera();
});

function fecharCamera() {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
  }
  video.srcObject = null;
  cameraModal.setAttribute("aria-hidden", "true");
}

// ==========================
// 4. CAPTURAR IMAGEM E ENVIAR
// ==========================
captureBtn.addEventListener("click", async () => {
  if (!stream) return alert("Câmera não iniciada.");

  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imagemBase64 = canvas.toDataURL("image/png");

  const nome = document.getElementById("nomeCadastro").value.trim();
  const curso = document.getElementById("curso").value.trim();
  const periodo = document.getElementById("periodo").value.trim();

  if (!nome || !curso || !periodo) {
    return alert("Preencha todos os campos!");
  }

  try {
    const resposta = await fetch("http://localhost:5000/cadastrar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nome,
        curso,
        periodo,
        imagem: imagemBase64,
      }),
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
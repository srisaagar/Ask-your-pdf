async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");
  const question = input.value.trim();
  if (!question) return;

  // USER MESSAGE
  const userRow = document.createElement("div");
  userRow.className = "msg-row user-row animate-pop";
  userRow.innerHTML = `<div class="bubble user-bubble">${question}</div>`;
  chatBox.appendChild(userRow);

  input.value = "";
  scrollBottom();

  // BOT MESSAGE
  const botRow = document.createElement("div");
  botRow.className = "msg-row bot-row animate-pop";
  botRow.innerHTML = `
    <div class="bubble bot-bubble">
      <span class="prefix">NEURAL STREAM</span>
      <span class="content">Analyzing document…</span>
    </div>
  `;
  chatBox.appendChild(botRow);
  scrollBottom();

  const content = botRow.querySelector(".content");

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    content.innerHTML = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      content.innerHTML += decoder.decode(value);
      scrollBottom();
    }

    addSuggestions();

  } catch {
    content.innerHTML = "⚠️ Neural stream interrupted.";
  }
}
function addSourceHint() {
  const chatBox = document.getElementById("chatBox");
  const hint = document.createElement("div");
  hint.className = "source-hint";
  hint.innerText = "📄 Answer grounded in uploaded document";
  chatBox.appendChild(hint);
  scrollBottom();
}


function addSuggestions() {
  const chatBox = document.getElementById("chatBox");

  const wrap = document.createElement("div");
  wrap.className = "suggestions";

  const items = [
    "Summarize the document",
    "Show total amount",
    "List all dates",
    "Explain in simple terms"
  ];

  items.forEach(text => {
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.innerText = text;
    chip.onclick = () => {
      document.getElementById("userInput").value = text;
      sendMessage();
    };
    wrap.appendChild(chip);
  });

  chatBox.appendChild(wrap);
  scrollBottom();
}

function scrollBottom() {
  const chatBox = document.getElementById("chatBox");
  chatBox.scrollTop = chatBox.scrollHeight;
}

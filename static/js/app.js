async function evaluateComment() {
  const comment = document.getElementById("comment").value;
  const resultDiv = document.getElementById("result");
  const qualityP = document.getElementById("quality").querySelector("p");
  const aspectsDiv = document.getElementById("aspects");
  const improvementTip = document.getElementById("improvement-tip");
  const sentimentIcon = document.getElementById("sentiment-icon");
  const hotelIcon = document.getElementById("quality").querySelector("svg");

  // Mostrar resultado e definir estado de carregamento
  resultDiv.classList.remove("hidden");
  qualityP.textContent = "Analisando...";
  aspectsDiv.innerHTML =
    "<div class='text-center'><i class='fas fa-spinner fa-spin'></i> Processando...</div>";
  improvementTip.textContent =
    "Analisando seu comentário para sugerir melhorias personalizadas...";

  try {
    const response = await fetch("/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ comment }),
    });
    const data = await response.json();

    if (data.error) {
      qualityP.textContent = `Erro: ${data.error}`;
      aspectsDiv.innerHTML = "";
      improvementTip.textContent =
        "Não foi possível gerar dicas. Tente novamente com outro comentário.";
      sentimentIcon.textContent = "❌";
      return;
    }

    // Definir ícone adequado para o sentimento
    if (data.quality === "positivo") {
      sentimentIcon.textContent = "😃";
      sentimentIcon.className = "text-3xl text-green-500";
      hotelIcon.parentElement.className = "w-8 h-8 mr-3 text-green-600";
    } else if (data.quality === "negativo") {
      sentimentIcon.textContent = "😞";
      sentimentIcon.className = "text-3xl text-red-500";
      hotelIcon.parentElement.className = "w-8 h-8 mr-3 text-red-600";
    } else {
      sentimentIcon.textContent = "😐";
      sentimentIcon.className = "text-3xl text-yellow-500";
      hotelIcon.parentElement.className = "w-8 h-8 mr-3 text-yellow-600";
    }

    // Mostrar qualidade
    qualityP.textContent = `Avaliação geral: ${
      data.quality.charAt(0).toUpperCase() + data.quality.slice(1)
    }`;

    // Criar cards para cada aspecto encontrado
    aspectsDiv.innerHTML = data.results
      .map(
        (r) => `
          <div class="p-3 rounded-lg ${getSentimentColor(
            r.sentiment
          )} flex items-center">
            <div class="mr-3 text-xl">${getSentimentEmoji(r.sentiment)}</div>
            <div>
              <div class="font-medium">${
                r.aspect.charAt(0).toUpperCase() + r.aspect.slice(1)
              }</div>
              <div class="text-sm">${
                r.sentiment.charAt(0).toUpperCase() + r.sentiment.slice(1)
              }${r.intensifier ? " (" + r.intensifier + ")" : ""}</div>
            </div>
          </div>
        `
      )
      .join("");

    // Gerar dica de melhoria baseada na análise
    improvementTip.textContent = generateImprovementTip(data);
  } catch (error) {
    qualityP.textContent = "Erro ao processar o comentário";
    aspectsDiv.innerHTML = "";
    improvementTip.textContent =
      "Não foi possível gerar dicas. Tente novamente mais tarde.";
    sentimentIcon.textContent = "❌";
  }
}

// Helper para obter cor de fundo baseada no sentimento
function getSentimentColor(sentiment) {
  switch (sentiment) {
    case "positivo":
      return "bg-green-100 text-green-800";
    case "negativo":
      return "bg-red-100 text-red-800";
    default:
      return "bg-yellow-100 text-yellow-800";
  }
}

// Helper para obter emoji baseado no sentimento
function getSentimentEmoji(sentiment) {
  switch (sentiment) {
    case "positivo":
      return "👍";
    case "negativo":
      return "👎";
    default:
      return "😐";
  }
}

// Gerar dica de melhoria baseada na análise
function generateImprovementTip(data) {
  // Encontrar aspectos negativos
  const negativos = data.results.filter((r) => r.sentiment === "negativo");
  const positivos = data.results.filter((r) => r.sentiment === "positivo");

  if (negativos.length === 0 && data.quality === "positivo") {
    return "Excelente trabalho! Continue mantendo o alto padrão de qualidade que seus hóspedes estão apreciando.";
  }

  if (negativos.length > 0) {
    const aspectosNegativos = negativos.map((n) => n.aspect).join(", ");
    return `Recomendamos melhorar os seguintes aspectos: ${aspectosNegativos}. Focar nestes pontos pode aumentar significativamente a satisfação dos hóspedes.`;
  }

  if (positivos.length > 0 && data.quality !== "positivo") {
    return "Há pontos positivos em seu estabelecimento, mas ainda há espaço para melhorias na experiência geral do hóspede.";
  }

  return "Analise os aspectos mencionados e trabalhe para melhorar a experiência geral dos hóspedes.";
}

// Exemplos predefinidos
const examples = [
  "O quarto foi ótimo.",
  "A localização é razoável.",
  "O serviço foi ruim.",
];

function useExample(index) {
  document.getElementById("comment").value = examples[index];
  evaluateComment();
}

// Contador de caracteres
document.getElementById("comment").addEventListener("input", function () {
  const charCount = this.value.length;
  document.getElementById("charCount").textContent = charCount;

  if (charCount > 500) {
    this.value = this.value.substring(0, 500);
    document.getElementById("charCount").textContent = "500";
  }
});

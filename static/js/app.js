async function evaluateComment() {
  const comment = document.getElementById("comment").value;
  const resultDiv = document.getElementById("result");
  const qualityP = document.getElementById("quality");
  const aspectsUl = document.getElementById("aspects");

  try {
    const response = await fetch("/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ comment }),
    });
    const data = await response.json();

    if (data.error) {
      resultDiv.classList.remove("hidden");
      qualityP.textContent = `Erro: ${data.error}`;
      aspectsUl.innerHTML = "";
      return;
    }

    resultDiv.classList.remove("hidden");
    qualityP.textContent = `Qualidade: ${
      data.quality.charAt(0).toUpperCase() + data.quality.slice(1)
    }`;
    aspectsUl.innerHTML = data.results
      .map(
        (r) =>
          `<li>${r.aspect}: ${r.sentiment}${
            r.intensifier ? " (" + r.intensifier + ")" : ""
          }</li>`
      )
      .join("");
  } catch (error) {
    resultDiv.classList.remove("hidden");
    qualityP.textContent = "Erro ao processar o comentário";
    aspectsUl.innerHTML = "";
  }
}

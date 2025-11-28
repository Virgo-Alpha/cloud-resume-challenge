document.addEventListener("DOMContentLoaded", () => {
  // ---------- THEME TOGGLE ----------
  const root = document.documentElement;
  const themeToggleBtn = document.getElementById("theme-toggle");

  const storedTheme = localStorage.getItem("theme");
  if (storedTheme === "light" || storedTheme === "dark") {
    root.setAttribute("data-theme", storedTheme);
  }

  themeToggleBtn.addEventListener("click", () => {
    const currentTheme = root.getAttribute("data-theme") || "light";
    const nextTheme = currentTheme === "light" ? "dark" : "light";
    root.setAttribute("data-theme", nextTheme);
    localStorage.setItem("theme", nextTheme);
  });

  // ---------- DOWNLOAD PDF (hosted file) ----------
  const downloadBtn = document.getElementById("download-pdf");
  downloadBtn.addEventListener("click", () => {
    const pdfUrl =
      "https://virgo-alpha.github.io/assets/docs/Benson_Mugure_Resume.pdf";
    // open in a new tab (user can download/save from there)
    window.open(pdfUrl, "_blank");
    // or, if you prefer same tab: window.location.href = pdfUrl;
  });

  // ---------- VISITOR COUNTER (placeholder) ----------
  /*
  const counterEl = document.getElementById("visitor-count");

  fetch("https://your-api-gateway-url.example.com/visitors", {
    method: "GET"
  })
    .then((res) => res.json())
    .then((data) => {
      counterEl.textContent = data.count ?? "—";
    })
    .catch((err) => {
      console.error("Failed to fetch visitor count:", err);
      counterEl.textContent = "—";
    });
  */
});

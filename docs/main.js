let pyodide = null;

async function main() {
  pyodide = await loadPyodide();

  // Load required Python files
  await pyodide.loadPackage(["micropip"]);
  const fs = pyodide.FS;

  // Fetch your Python files and write them into the Pyodide filesystem
  const files = ["puissance4jeu.py", "algo4_puissancen_thread.py"];
  for (let file of files) {
    const response = await fetch(`./py/${file}`);
    const content = await response.text();
    fs.writeFile(file, content);
  }

  document.getElementById("run-button").addEventListener("click", async () => {
    try {
      const output = await pyodide.runPythonAsync(`
import sys
from io import StringIO
sys.stdout = StringIO()

# Import your game logic
import algo4_puissancen_thread
import puissance4jeu

sys.stdout.getvalue()
      `);
      document.getElementById("output").textContent = output;
    } catch (err) {
      document.getElementById("output").textContent = "Error: " + err;
    }
  });
}

main();


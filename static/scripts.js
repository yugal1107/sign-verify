function showLoading(button) {
  const originalText = button.innerHTML;
  button.disabled = true;
  button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
  return originalText;
}

function hideLoading(button, originalText) {
  button.disabled = false;
  button.innerHTML = originalText;
}

// Update file input label
document
  .querySelector('input[type="file"]')
  .addEventListener("change", function (e) {
    const fileName = e.target.files[0]?.name || "No file chosen";
    document.querySelector(
      ".file-label"
    ).innerHTML = `<i class="fas fa-file"></i> ${fileName}`;
  });

// Fetch and display the public key
fetch("/public_key")
  .then((response) => response.text())
  .then((publicKey) => {
    document.getElementById("publicKey").innerText = publicKey;
  })
  .catch((error) => {
    console.error("Error fetching public key:", error);
    document.getElementById("publicKey").innerHTML =
      '<span style="color: red;"><i class="fas fa-exclamation-triangle"></i> Error loading public key</span>';
  });

document.getElementById("signForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const button = this.querySelector("button");
  const originalText = showLoading(button);

  var formData = new FormData(this);
  fetch("/sign", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.blob())
    .then((blob) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = "signature.sig";
      document.body.appendChild(a);
      a.click();
      a.remove();
      document.getElementById("signResult").innerHTML =
        '<span style="color: green;"><i class="fas fa-check-circle"></i> Document signed successfully!</span>';
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("signResult").innerHTML =
        '<span style="color: red;"><i class="fas fa-exclamation-triangle"></i> Error signing document</span>';
    })
    .finally(() => {
      hideLoading(button, originalText);
    });
});

document.getElementById("verifyForm").onsubmit = async function (event) {
  event.preventDefault();
  const button = this.querySelector("button");
  const originalText = showLoading(button);

  const formData = new FormData(this);
  const response = await fetch("/verify", {
    method: "POST",
    body: formData,
  });
  const result = await response.json();
  document.getElementById("verifyResult").innerText = result.message;
  hideLoading(button, originalText);
};

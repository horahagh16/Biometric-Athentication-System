document.getElementById("process").addEventListener("change", function() {
    const process = this.value;
    const mnemonicGroup = document.getElementById("mnemonicGroup");

    if (process === "login") {
        mnemonicGroup.style.display = "block";
    } else {
        mnemonicGroup.style.display = "none";
    }
});

document.getElementById("authForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("process", document.getElementById("process").value);
    formData.append("faceImage", document.getElementById("faceImage").files[0]);
    formData.append("fingerImage", document.getElementById("fingerImage").files[0]);
    formData.append("passphrase", document.getElementById("passphrase").value);

    if (document.getElementById("process").value === "login") {
        formData.append("mnemonic", document.getElementById("mnemonic").value);
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/process_biometrics", true);
    
    xhr.onload = function() {
        const responseDiv = document.getElementById("response");

        if (xhr.status === 200) {
            responseDiv.textContent = xhr.responseText;

            if (xhr.responseText.includes("UNSUCCESSFUL AUTHENTICATION")) {
                responseDiv.className = "error";
            } else {
                responseDiv.className = "success"; 
            }
        } else {
            responseDiv.textContent = "An error occurred. Please try again.";
            responseDiv.className = "error"; 
        }
    };

    xhr.send(formData);
});

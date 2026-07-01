function setupPasswordStrength(inputId, barId, textId, errorId) {
    const input = document.getElementById(inputId);
    const bar = document.getElementById(barId);
    const text = document.getElementById(textId);

    let lastLevel = "";

    input.addEventListener("input", function () {
        const result = checkPasswordStrength(this.value);

        bar.style.width = result.width;
        bar.style.backgroundColor = result.color;

        if (this.value.trim() === "") {
            text.style.display = "none";
        } else {
            text.style.display = "block";
            text.textContent = "Password Strength: " + result.label;
        }

        if (this.value.trim() !== "") {
            clearPasswordInvalid(inputId, errorId);
        }

        if (result.label !== "-" && result.label !== lastLevel) {
            if (result.label === "Weak") {
                showToast("Warning: Your password is still weak", "warning");
            } else if (result.label === "Medium") {
                showToast("Your password is fairly secure", "warning");
            } else if (result.label === "Strong") {
                showToast("Great! Your password is strong", "success");
            } else if (result.label === "Very Strong") {
                showToast("Excellent! Your password is very strong", "success");
            }

            lastLevel = result.label;
        }
    });
}
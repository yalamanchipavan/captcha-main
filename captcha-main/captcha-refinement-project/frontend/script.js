document.addEventListener("DOMContentLoaded", function () {
    const captchaImage = document.getElementById("captchaImage");
    const refreshButton = document.getElementById("refreshButton");
    const captchaInput = document.getElementById("captchaInput");
    const submitButton = document.getElementById("submitButton");
    let captchaId = null;

    function loadCaptcha() {
        fetch("http://127.0.0.1:5000/get_captcha")
            .then(response => response.json())
            .then(data => {
                captchaId = data.captcha_id;
                captchaImage.src = `http://127.0.0.1:5000${data.image_url}`;
            })
            .catch(error => console.error("Error fetching CAPTCHA:", error));
    }

    refreshButton.addEventListener("click", loadCaptcha);

    submitButton.addEventListener("click", function () {
        const userCaptcha = captchaInput.value.trim();

        if (!userCaptcha) {
            alert("Please enter the CAPTCHA.");
            return;
        }

        fetch("http://127.0.0.1:5000/validate_captcha", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ captcha_id: captchaId, captcha_text: userCaptcha })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("CAPTCHA Verified Successfully!");
                    captchaInput.value = "";
                    loadCaptcha();
                } else {
                    alert("Incorrect CAPTCHA. Try again.");
                }
            })
            .catch(error => console.error("Error validating CAPTCHA:", error));
    });

    loadCaptcha();
});

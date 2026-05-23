const btn = document.getElementById("generateBtn");

btn.addEventListener("click", async () => {

    const linkedinUrl =
        document.getElementById("linkedinUrl").value;

    const formData = new FormData();

    formData.append(
        "linkedin_url",
        linkedinUrl
    );

    const response = await fetch(
        "http://localhost:9000/cold-email",
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    document.getElementById("output").innerText =
        data.email;
});
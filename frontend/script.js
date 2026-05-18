const uploadBtn = document.getElementById("uploadBtn");
const pdfInput = document.getElementById("pdfInput");
const statusText = document.getElementById("status");

uploadBtn.addEventListener("click", async () => {

    const file = pdfInput.files[0];

    if (!file) {
        alert("Select a PDF first");
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    statusText.innerText = "Uploading...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        console.log(data);

        statusText.innerText =
            "Uploaded: " + data.filename;

    } catch (error) {

        console.error(error);

        statusText.innerText =
            "Upload failed";
    }

});
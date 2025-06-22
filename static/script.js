document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('uploadForm')
    if(!form) return;

    form.addEventListener("submit", async(e) => {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            if(response.ok) {
                console.log("Datei erfolgreich hochgeladen");
                location.reload();
            } else {
                console.error("Fehler beim Hochladen");
            }
        } catch (err) {
            console.error("Netzwerkfehler:", err);
        }
    });
});


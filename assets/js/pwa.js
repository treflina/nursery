let deferredPrompt;
window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;

    const header = document.querySelector(".profile-container");
    const installButton = document.createElement("button");

    const icon = '<svg xmlns="http://www.w3.org/2000/svg" title="Zainstaluj aplikację" class="w-6 h-6" viewBox="0 0 512 512"><path d="M 280 24 Q 278 2 256 0 Q 234 2 232 24 L 232 294 L 232 294 L 137 199 L 137 199 Q 120 185 103 199 Q 89 216 103 233 L 239 369 L 239 369 Q 256 383 273 369 L 409 233 L 409 233 Q 423 216 409 199 Q 392 185 375 199 L 280 294 L 280 294 L 280 24 L 280 24 Z M 129 304 L 64 304 L 129 304 L 64 304 Q 37 305 19 323 Q 1 341 0 368 L 0 448 L 0 448 Q 1 475 19 493 Q 37 511 64 512 L 448 512 L 448 512 Q 475 511 493 493 Q 511 475 512 448 L 512 368 L 512 368 Q 511 341 493 323 Q 475 305 448 304 L 383 304 L 383 304 L 335 352 L 335 352 L 448 352 L 448 352 Q 463 353 464 368 L 464 448 L 464 448 Q 463 463 448 464 L 64 464 L 64 464 Q 49 463 48 448 L 48 368 L 48 368 Q 49 353 64 352 L 177 352 L 177 352 L 129 304 L 129 304 Z M 432 408 Q 430 386 408 384 Q 386 386 384 408 Q 386 430 408 432 Q 430 430 432 408 L 432 408 Z" /></svg>'

    installButton.innerHTML = icon

    installButton.classList.add("btn-profile");

    installButton.addEventListener("click", async () => {
        if (deferredPrompt !== null) {
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            if (outcome === "accepted") {
                deferredPrompt = null;
            }
        }
        installButton.style.display = "none";
    });

        header?.appendChild(installButton);
    });
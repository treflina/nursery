(() => {
    let modal, targetModal;
    const wrapper = document.querySelector(".modal-wrapper")
    const openModalBtns = document.querySelectorAll(".openModal");
    const cancelBtns = document.querySelectorAll(".cancelBtn");
    const modalBackground = document.querySelector(".modalBackground");


    const openModal = (e) => {
        e.preventDefault();
        targetModal = e.currentTarget.getAttribute("data-target");
        modal = document.querySelector(`${targetModal}`);
        modal.classList.remove("hidden");
        modalBackground.classList.remove("hidden");
        modal.focus();
        !modal.classList.contains("no-inert") && wrapper.setAttribute("inert", "");
    }

    const closeModal = () => {
        modal.classList.add("hidden");
        modalBackground.classList.add("hidden");
        wrapper.removeAttribute("inert")
        const openModalBtn = document.querySelector(`[data-target="${targetModal}"]`)
        openModalBtn.focus()
    }

    openModalBtns.forEach((btn) =>
        btn.addEventListener("click", openModal)
    )

    cancelBtns.forEach((btn) =>
        btn.addEventListener("click", closeModal)
    )

    modalBackground.addEventListener("click", closeModal)
    window.addEventListener("keyup", (e) => {
        if (e.key === "Escape" && !modal.classList.contains("hidden")) {
            closeModal()
        }
        })

}) ();
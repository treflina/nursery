(() => {
    let modal, targetModal;
    const wrapper = document.querySelector(".modal-wrapper")
    const openModalBtns = document.querySelectorAll(".openModal");
    const cancelBtns = document.querySelectorAll(".cancelBtn");
    // const modal = document.getElementById("modal");
    const modalBackground = document.querySelector(".modalBackground");


    const openModal = (e) => {
        e.preventDefault();
        targetModal = e.currentTarget.getAttribute("data-target");
        modal = document.querySelector(`${targetModal}`);
        modal.classList.remove("hidden");
        modalBackground.classList.remove("hidden");
        modal.focus();
        wrapper.setAttribute("inert", "");
    }

    const closeModal = () => {
        modal.classList.add("hidden");
        modalBackground.classList.add("hidden");
        wrapper.removeAttribute("inert")
        const openModalBtn = document.querySelector(`[data-target="${targetModal}"]`)
        console.log(openModalBtn)
        openModalBtn.focus()
    }

    openModalBtns.forEach((btn) =>
        btn.addEventListener("click", openModal)
    )

    cancelBtns.forEach((btn) =>
        btn.addEventListener("click", closeModal)
    )


    // openModalBtn.addEventListener("click", openModal)
    // cancelBtn.addEventListener("click", closeModal)
    modalBackground.addEventListener("click", closeModal)
    window.addEventListener("keyup", (e) => {
        if (e.key === "Escape" && !modal.classList.contains("hidden")) {
            closeModal()
        }
        })
    // let modal;
    // const body = document.querySelector("body");

    // const openModal = document.querySelectorAll(".openModal");
    // const closeModal = document.querySelectorAll(".close");
    // const modalContent = document.querySelector(".modal__content");

    // const close = (e) => {
    //     e.preventDefault();
    //     modal?.classList.remove("show");
    //     modal?.classList.add("hide");
    //     body.style.overflowY = "scroll";
    // };

    // openModal.forEach((btn) =>
    //     btn.addEventListener("click", (e) => {
    //         e.preventDefault();
    //         const targetModal = e.currentTarget.getAttribute("data-target");

    //         modal = document.querySelector(`${targetModal}`);
    //         modal.classList.add("show");
    //         modal.classList.remove("hide");
    //         body.style.overflowY = "hidden";
    //     })
    // );

    // closeModal.forEach((btn) => btn.addEventListener("click", close));

    // document.addEventListener("keydown", (e) => {
    //     if (e.key === "Escape") {
    //         close(e);
    //     }
    // });
}) ();
import Swal from 'sweetalert2';

(() => {
    let wrapper, modalBackground, modal;

    const Toast = Swal.mixin({
            toast: true,
            timerProgressBar: true,
            timer: 3000,
            position: "bottom-end",
            showConfirmButton: false,
            didOpen: (toast) => {
                toast.onmouseenter = Swal.stopTimer;
                toast.onmouseleave = Swal.resumeTimer;
            }
        })

    const closeModal = () => {
        modal.classList.add("hidden");
        modal.innerHTML = "";
        modalBackground.classList.add("hidden");
        wrapper.removeAttribute("inert");
    }

    const openModal = (e) => {
        modal.classList.remove("hidden");
        modalBackground.classList.remove("hidden");
        modal.focus();
        !modal.classList.contains("no-inert") && wrapper.setAttribute("inert", "");
    }

    // htmx.logAll();

    document.addEventListener("htmx:beforeSwap", (e) => {
        if (e.detail.target.id == "modal" && (!e.detail.xhr.response || e.detail.xhr.response == "")) {
            closeModal()
            e.detail.shouldSwap = false
        }
    })

    document.addEventListener("htmx:afterSettle", (e) => {

        const cancelBtns = document.querySelectorAll(".cancelBtn");

        if (e.detail.target.id === "modal") {
            openModal()
        }

        cancelBtns?.forEach((btn) =>
            btn.addEventListener("click", closeModal)
        );

        modalBackground?.addEventListener("click", closeModal)
        window.addEventListener("keyup", (e) => {
            if (e.key === "Escape" && !modal?.classList.contains("hidden")) {
                closeModal()
            }
        })
    })

    document.addEventListener("htmx:load", () => {
        // for parent form modals (not swal)
        wrapper = document.querySelector(".modal-wrapper")
        modalBackground = document.querySelector(".modalBackground");
        modal = document.querySelector("#modal");

         // Show swal pop-up info about absent children
        const absentTodayInfoBtn = document.querySelector(".absentToday");
        const absentTomorrowInfoBtn = document.querySelector(".absentTomorrow");

        const absenceInfoOptions = {
            buttonsStyling: false,
            confirmButtonText: "Zamknij",
            customClass: {
                title: "text-xl",
                confirmButton: "flex items-center font-semibold h-11 px-2 gap-1 border-2 border-neutral-300 \
              rounded-md bg-amber-100 hover:bg-amber-200  \
              !duration-300 !transition-colors",
            }
        }

        absentTodayInfoBtn?.addEventListener("click", (e) => {
            e.preventDefault();
            Swal.fire(
                {
                    template: "#absent-today-info",
                    ...absenceInfoOptions
                }
            )
        }
        );

        absentTomorrowInfoBtn?.addEventListener("click", (e) => {
            e.preventDefault();
            Swal.fire(
                {
                    template: "#absent-tomorrow-info",
                    ...absenceInfoOptions
                }
            )
        }
        );
    });

    // Delete absence confirmation
    document.addEventListener('htmx:confirm', function (evt) {
        if (!evt.detail.elt.hasAttribute('confirm-swal') && !evt.detail.elt.hasAttribute('confirm-swal2')) {
            return
        }

        const question = evt.detail.elt.getAttribute('confirm-swal') || evt.detail.elt.getAttribute('confirm-swal2');
        const swalTile = evt.detail.elt.getAttribute('title-swal')
        const swalExpl = evt.detail.elt.getAttribute('expl-swal')

        const nextElementToFocus = (
            evt.detail.elt.closest('tr')?.nextElementSibling?.querySelector("a")
        ) ?? (evt.detail.elt.closest('tr')?.previousElementSibling?.querySelector("button")
            ) ?? document.querySelector(".pagination")?.querySelector("button");

        evt.preventDefault();

        const iconSvg = `<svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"></path>
                        </svg>`;

        const questionSvg = `<svg class="h-6 w-6 text-green-800" fill="green" stroke-width="1.5" stroke="currentColor" aria-hidden="true" viewBox="0 0 288 448">
                                <path d="M 64 128 Q 65 101 83 83 L 83 83 L 83 83 Q 101 65 128 64 L 160 64 L 160 64 Q 187 65 205 83 Q 223 101 224 128 L 224 132 L 224 132 Q 223 166 195 185 L 152 213 L 152 213 Q 113 239 112 287 L 112 288 L 112 288 Q 112 302 121 311 Q 130 320 144 320 Q 158 320 167 311 Q 176 302 176 288 L 176 287 L 176 287 Q 176 274 187 266 L 229 239 L 229 239 Q 257 221 272 193 Q 288 165 288 131 L 288 128 L 288 128 Q 287 74 251 37 Q 214 1 160 0 L 128 0 L 128 0 Q 74 1 37 37 Q 1 74 0 128 Q 0 142 9 151 Q 18 160 32 160 Q 46 160 55 151 Q 64 142 64 128 L 64 128 Z M 144 448 Q 167 447 179 428 Q 189 408 179 388 Q 167 369 144 368 Q 121 369 109 388 Q 99 408 109 428 Q 121 447 144 448 L 144 448 Z" />
                            </svg>`

        const text = question.includes("zatwierdzić") || question.includes("wysłać")  ? "Czy na pewno" : "Czy na pewno usunąć"
        Swal.fire({
            title: swalTile || "Ostrzeżenie",
            html: [`${text} ${question}?`, `${swalExpl || ""}`].join("<br class='mb-2'>"),
            showCancelButton: true,
            cancelButtonText: "Wróć",
            confirmButtonText: "Tak",
            buttonsStyling: false,
            icon: "warning",
            iconHtml: swalTile ? questionSvg : iconSvg,
            position: "top",
            customClass: {
                popup: "!relative !transform !overflow-hidden !rounded-lg !bg-white !text-left !shadow-xl !transition-all sm:!my-8 sm:!w-full sm:!max-w-lg !p-0 !grid-cols-none",
                icon: '!m-0 !mx-auto !flex !h-12 !w-12 !flex-shrink-0 !items-center !justify-center !rounded-full !border-0 !bg-red-100 sm:!h-10 sm:!w-10 !mt-5 sm!mt-6 sm:!ml-6 !col-start-1 !col-end-3 sm:!col-end-2',
                title: "!p-0 !pt-3 !text-center sm:!text-left !text-xl !font-semibold !leading-6 !text-gray-900 !pl-4 !pr-4 sm:!pr-6 sm:!pl-0 sm:!pt-6 sm:!ml-4 !col-start-1 sm:!col-start-2 !col-end-3",
                htmlContainer: "!mt-2 sm:!mt-0 !m-0 !text-base !text-center sm:!text-left !text-gray-800 !pl-4 sm:!pl-0 !pr-4 !pb-4 sm:!pr-6 sm:!pb-4 sm:!ml-4 !col-start-1 sm:!col-start-2 !col-end-3",
                actions: "!bg-gray-50 !px-4 !py-3 sm:!flex sm:!flex-row-reverse sm:!px-6 !w-full !justify-start !mt-0 !col-start-1 !col-end-3",
                confirmButton: "inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto",
                cancelButton: "mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto",
            }
        }).then((result) => {
            if (result.isConfirmed) {
                nextElementToFocus?.focus();
                evt.detail.issueRequest(true);
            }
        });
    });

    document.addEventListener("showToast", function (evt) {
        const message = evt.detail.msg
        const bcg = evt.detail.err && "rgb(254 226 226)"

        Toast.fire({
            background: bcg || "#e0f6e2",
            text: message || "Data has been successfully changed.",
        })
    })

    document.addEventListener("billingsDeleted", function (e) {
        console.log("deleted")
        // window.replaceState({}, "", "/billings/")
    })
})();
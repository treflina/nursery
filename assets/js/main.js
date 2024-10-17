import Datepicker from "flowbite-datepicker/Datepicker";
import DateRangePicker from "flowbite-datepicker/DateRangePicker";
import pl from "../../node_modules/flowbite-datepicker/js/i18n/locales/pl"


document.addEventListener("createAbsenceForm", function (e) {
    Datepicker.locales.pl = pl.pl;

    const datepickerOptions = {
        allowOneSidedRange: true,
        language: "pl",
        weekStart: 1,
        format: "dd.mm.yyyy",
        orientation: "bottom",
        todayHighlight: true,
        autohide: true,
        clearButton: true,
    };

    const today = new Date();

    if (e.target.matches("#btn-abs")) {
        datepickerOptions.minDate = today
    }

    const daterangepicker = document.querySelector(".daterangepicker");
    const datepickerStart = document.querySelector(".datepicker1");
    const rangePicker = new DateRangePicker(daterangepicker, datepickerOptions);

    const setEndValue = () => {
        let endValue;

        const startValue = datepickerStart?.value;
        const [day, month, year] = [...startValue.split(".")];
        const monthNum = parseInt(month);
        const startValueDate = new Date(year, monthNum - 1, day);
        endValue = startValueDate;

        rangePicker.setDates(startValue, endValue);
    };

    datepickerStart?.addEventListener("changeDate", setEndValue);
    datepickerStart?.addEventListener("focus", () => {
        rangePicker.datepickers[1].setDate({ clear: true });
    });

    // "first day paid" checkbox dependent on absence type
    const absenceTypeSelect = document.querySelector("#id_absence_type");

    absenceTypeSelect?.addEventListener("change", (e) => {
        const firstDayCheckbox = document.querySelector("#id_first_day_paid");
        const firstDayLabel = document.querySelector(".first-day-label");

        if (e.target.value !== "R") {
            firstDayLabel.classList.add("text-neutral-500");
            firstDayLabel.classList.remove("text-black");
            firstDayCheckbox.setAttribute("disabled", true);
        } else {
            firstDayLabel.classList.add("text-black");
            firstDayLabel.classList.remove("text-neutral-500");
            firstDayCheckbox.removeAttribute("disabled");
        }
    })
});

document.addEventListener("htmx:afterSettle", function (e) {
    const btnGetBilling = document.querySelector(".btn-bill");

    if (btnGetBilling) {
        if (e.detail.pathInfo.requestPath.startsWith("/billing")) {
            btnGetBilling.style.display = "none";
        } else {
            btnGetBilling.style.display = "block";
        }
    }
});

document.addEventListener("changedDate", function (evt) {
    const chosenDate = new Date(Date.parse(evt.detail.chosendate));
    chosenDate.setHours(0, 0, 0, 0);
    const numDate = `${chosenDate.getDate()}`;
    const calendarDays = document.querySelectorAll(".cal-day")
    const btnAbsenceForm = document.querySelector("#btn-abs")

    const today = new Date()
    today.setHours(0, 0, 0, 0);
    if (btnAbsenceForm) {
        if (today > chosenDate) {
            btnAbsenceForm.style.display = "none";
        } else {
            btnAbsenceForm.style.display = "block";
        }
    }

    calendarDays.forEach(day => {
        if (day.innerHTML === numDate) {
            day.classList.add("font-bold")
        } else {
            day.classList.remove("font-bold")
        }
    })
})

document.addEventListener("success", function (evt) {

    const formContainer = document.querySelector("#absence-form")
    const successMsg = document.createElement("h3")

    successMsg.innerHTML = "Thank you for submitting!"

    formContainer.appendChild(successMsg)

    console.log("success")
})

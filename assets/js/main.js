import Datepicker from "flowbite-datepicker/Datepicker";
import DateRangePicker from "flowbite-datepicker/DateRangePicker";
// import pl from "../../node_modules/flowbite-datepicker/js/i18n/locales/pl"
import pl from "flowbite-datepicker/locales/pl";
import Alpine from 'alpinejs'

(() => {
    window.Alpine = Alpine
    Alpine.start()

    // document.addEventListener("DOMContentLoaded", function () {
    //     htmx.logAll();
    // });

    document.addEventListener("createAbsenceForm", function (e) {
        Datepicker.locales.pl = pl.pl

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
        const rangePicker = new DateRangePicker(daterangepicker, datepickerOptions);
        const datepickerStart = document.querySelector(".datepicker1");

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
        const numDate = `${chosenDate.getDate()}`;
        const month = `${chosenDate.getMonth() + 1}`;
        const displayedMonth = document.querySelector(".monthHeading").dataset.month
        const calendarDays = document.querySelectorAll(".cal-day")

        if (displayedMonth > month) {
            const prevMonthBtn = document.querySelector(".prevMonth");
            prevMonthBtn.click();
        }

        if (displayedMonth < month){
            const nextMonthBtn = document.querySelector(".nextMonth");
            nextMonthBtn.click()
        }

        calendarDays.forEach(day => {
            if (day.innerHTML === numDate) {
                day.classList.add("font-bold")
            } else {
                day.classList.remove("font-bold")
            }
        })
    });

})();

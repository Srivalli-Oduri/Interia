document.addEventListener("DOMContentLoaded", () => {

    const steps = document.querySelectorAll(".step");
    const title = document.querySelector(".steps h3");
    const desc = document.querySelector(".steps p");
    const image = document.querySelector(".steps-image img");

    const stepData = [
        {
            title: "Meet our designer",
            desc: "Discuss your design needs with our expert team",
            img: "source/how-m1-1.jpg"
        },
        {
            title: "Design finalization",
            desc: "Finalize layouts, materials and budget",
            img: "source/how-m1-2.jpg"
        },
        {
            title: "Order confirmation",
            desc: "Confirm designs and place the order",
            img: "source/how-m1-3.jpg"
        },
        {
            title: "Installation begins",
            desc: "Our team starts installing your interiors",
            img: "source/how-m1-4.jpg"
        },
        {
            title: "Move in",
            desc: "Your dream home is ready to live in",
            img: "source/how-m1-5.jpg"
        }
    ];

    let current = 0;

    function showStep(index) {
        steps.forEach(step => step.classList.remove("active"));
        steps[index].classList.add("active");

        title.textContent = stepData[index].title;
        desc.textContent = stepData[index].desc;

        image.style.opacity = "0";
        image.style.transform = "scale(0.95)";

        setTimeout(() => {
            image.src = stepData[index].img;
            image.style.opacity = "1";
            image.style.transform = "scale(1)";
        }, 250);
    }

    // AUTO ANIMATION (1 → 2 → 3 → 4 → 5)
    setInterval(() => {
        current = (current + 1) % steps.length;
        showStep(current);
    }, 3000); // matches video speed

    // MANUAL CLICK SUPPORT
    steps.forEach((step, index) => {
        step.addEventListener("click", () => {
            current = index;
            showStep(index);
        });
    });

    // Initial
    showStep(0);
});
console.log("Footer loaded");

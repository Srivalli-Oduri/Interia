document.addEventListener("DOMContentLoaded", function () {

    const steps = document.querySelectorAll(".step");
    const title = document.querySelector(".step-content h3");
    const desc = document.querySelector(".step-content p");
    const img = document.querySelector(".steps-image img");

    const data = [
        {
            title: "Meet our designer",
            desc: "Discuss your design needs with our expert team",
            img: "/static/images/how-m1-1.jpg"
        },
        {
            title: "Design finalization",
            desc: "Finalize layouts, materials and budget",
            img: "/static/images/how-m1-2.jpg"
        },
        {
            title: "Order confirmation",
            desc: "Confirm designs and place the order",
            img: "/static/images/how-m1-3.jpg"
        },
        {
            title: "Installation begins",
            desc: "Our team starts installing your interiors",
            img: "/static/images/how-m1-4.jpg"
        },
        {
            title: "Move in",
            desc: "Your dream home is ready to live in",
            img: "/static/images/how-m1-5.jpg"
        }
    ];

    let current = 0;

    function updateStep(index) {
        steps.forEach(s => s.classList.remove("active"));
        steps[index].classList.add("active");

        title.textContent = data[index].title;
        desc.textContent = data[index].desc;

        img.style.opacity = "0";
        setTimeout(() => {
            img.src = data[index].img;
            img.style.opacity = "1";
        }, 300);
    }

    // AUTO PLAY
    setInterval(() => {
        current = (current + 1) % steps.length;
        updateStep(current);
    }, 3000);

    // CLICK SUPPORT
    steps.forEach((step, index) => {
        step.addEventListener("click", () => {
            current = index;
            updateStep(index);
        });
    });

    updateStep(0);
});
console.log("Footer loaded");
const openQuote = document.getElementById("openQuote");
const overlay = document.getElementById("quoteOverlay");
const card = document.getElementById("quoteCard");
const closeQuote = document.getElementById("closeQuote");

/* Open */
openQuote.addEventListener("click", () => {
    overlay.style.display = "flex";
    document.body.classList.add("lock");
});

/* Close */
closeQuote.addEventListener("click", () => {
    overlay.style.display = "none";
    document.body.classList.remove("lock");
});

/* Click outside */
overlay.addEventListener("click", e => {
    if (e.target === overlay) {
        overlay.style.display = "none";
        document.body.classList.remove("lock");
    }
});

/* Mouse movement (UP & DOWN EFFECT) */
document.addEventListener("mousemove", e => {
    if (overlay.style.display === "flex") {
        const y = (window.innerHeight / 2 - e.clientY) / 30;
        card.style.transform = `translateY(${y}px)`;
    }
});
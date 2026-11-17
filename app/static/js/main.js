
document.addEventListener("DOMContentLoaded", () => {
    // Automatically dismiss flash messages after 5 seconds.
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.4s ease";
            alert.style.opacity = "0";

            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });
});

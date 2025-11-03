document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) { return new bootstrap.Tooltip(tooltipTriggerEl); });
    // Pulse animation on page load for circles
    document.querySelectorAll('.circular-chart').forEach(el => {
        el.classList.add('pulse');
    });
});
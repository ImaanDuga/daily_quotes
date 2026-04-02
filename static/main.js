const slides = document.querySelectorAll('.slide');
const dotsContainer = document.getElementById('dots');
let current = 0;
let timer;

// Build dots
slides.forEach((_, i) => {
    const dot = document.createElement('div');
    dot.classList.add('dot');
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goTo(i));
    dotsContainer.appendChild(dot);
});

function getDots() {
    return document.querySelectorAll('.dot');
}

function goTo(index) {
    slides[current].classList.remove('active');
    getDots()[current].classList.remove('active');
    current = index;
    slides[current].classList.add('active');
    getDots()[current].classList.add('active');
    resetTimer();
}

function next() {
    goTo((current + 1) % slides.length);
}

function resetTimer() {
    clearInterval(timer);
    timer = setInterval(next, 5000);
}

// Start
resetTimer();

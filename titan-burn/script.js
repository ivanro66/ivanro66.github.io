// === Detección de dispositivo ===
function esMovil() {
  return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// === Pausar animaciones si la pestaña no está activa ===
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    cancelAnimationFrame(animFrutas);
    cancelAnimationFrame(animCubos);
  } else {
    animateFrutas();
    animateCubos();
  }
});

// === Partículas interactivas ===
const cantidadParticulas = esMovil() ? 40 : 80;

tsParticles.load("particles-js", {
  fullScreen: { enable: false },
  particles: {
    number: { value: cantidadParticulas },
    size: { value: 3 },
    move: { enable: true, speed: 1 },
    color: { value: "#ffffff" },
    links: { enable: true, color: "#ffffff" },
  },
  interactivity: {
    events: { onHover: { enable: true, mode: "repulse" } },
    modes: { repulse: { distance: 100 } },
  },
});

// === Slider ===
let currentSlide = 0;
let direction = 1;
const slider = document.querySelector('.slider');
const totalSlides = document.querySelectorAll('.slide').length;

function goToSlide(index) {
  currentSlide = (index + totalSlides) % totalSlides;
  slider.style.transform = `translateX(-${currentSlide * 100}vw)`;
}

document.getElementById('next').addEventListener('click', () => {
  direction = 1;
  goToSlide(currentSlide + 1);
});

document.getElementById('prev').addEventListener('click', () => {
  direction = -1;
  goToSlide(currentSlide - 1);
});

setTimeout(() => {
  setInterval(() => {
    if (currentSlide === totalSlides - 1) {
      direction = -1;
    } else if (currentSlide === 0) {
      direction = 1;
    }
    goToSlide(currentSlide + direction);
  }, 10000);
}, 10000);

// === Frutas flotantes dinámicas ===
const frutaSources = [
  { src: 'assets/citricos-slides.png' },
  { src: 'assets/citricos-slides2.png' },
  { src: 'assets/mango.png', class: 'mango' },
  { src: 'assets/pina.png' },
  { src: 'assets/sandia-slides.png' }
];

const frutasContainer = document.querySelector('.frutas');
const totalFrutas = esMovil() ? 6 : 14;
const frutas = [];

for (let i = 0; i < totalFrutas; i++) {
  const frutaData = frutaSources[i % frutaSources.length];
  const fruta = document.createElement('img');
  fruta.src = frutaData.src;
  fruta.className = 'fruta' + (frutaData.class ? ' ' + frutaData.class : '');

  const size = 60 + Math.random() * 24;
  fruta.style.width = `${size}px`;
  fruta.style.left = Math.random() * 90 + '%';
  fruta.style.top = Math.random() * 80 + '%';

  frutasContainer.appendChild(fruta);

  frutas.push({
    el: fruta,
    x: parseFloat(fruta.style.left),
    y: parseFloat(fruta.style.top),
    dx: (Math.random() - 0.5) * 0.6,
    dy: (Math.random() - 0.5) * 0.6,
    rotation: Math.random() * 360,
    dr: (Math.random() - 0.5) * 1.5
  });
}

let animFrutas;
function animateFrutas() {
  frutas.forEach(f => {
    f.x += f.dx;
    f.y += f.dy;
    f.rotation += f.dr;

    if (f.x < 0 || f.x > 95) f.dx *= -1;
    if (f.y < 0 || f.y > 90) f.dy *= -1;

    f.el.style.left = f.x + '%';
    f.el.style.top = f.y + '%';
    f.el.style.transform = `rotate(${f.rotation}deg)`;
  });

  animFrutas = requestAnimationFrame(animateFrutas);
}
animateFrutas();

// === Cubos de hielo flotantes ===
const cuboSources = [
  { src: 'assets/cubo-hielo.png' },
  { src: 'assets/cubo2-hielo.png' },
  { src: 'assets/hielos.png', once: true }
];

const cubosContainer = document.querySelector('.cubos');
const totalCubos = esMovil() ? 5 : 12;
const cubos = [];

for (let i = 0; i < totalCubos; i++) {
  let cuboData = (i === 0) ? cuboSources.find(c => c.once) : cuboSources[i % 2];
  const cubo = document.createElement('img');
  cubo.src = cuboData.src;
  cubo.className = 'cubo';

  const size = 60 + Math.random() * 24;
  cubo.style.width = `${size}px`;
  cubo.style.left = Math.random() * 90 + '%';
  cubo.style.top = Math.random() * 80 + '%';

  cubosContainer.appendChild(cubo);

  cubos.push({
    el: cubo,
    x: parseFloat(cubo.style.left),
    y: parseFloat(cubo.style.top),
    dx: (Math.random() - 0.5) * 0.6,
    dy: (Math.random() - 0.5) * 0.6,
    rotation: Math.random() * 360,
    dr: (Math.random() - 0.5) * 1.5
  });
}

let animCubos;
function animateCubos() {
  cubos.forEach(c => {
    c.x += c.dx;
    c.y += c.dy;
    c.rotation += c.dr;

    if (c.x < 0 || c.x > 95) c.dx *= -1;
    if (c.y < 0 || c.y > 90) c.dy *= -1;

    c.el.style.left = c.x + '%';
    c.el.style.top = c.y + '%';
    c.el.style.transform = `rotate(${c.rotation}deg)`;
  });

  animCubos = requestAnimationFrame(animateCubos);
}
animateCubos();

// === Brasas flotantes en sección burn ===
const brasasContainer = document.querySelector('.slide.burn .brasas');
const totalBrasas = esMovil() ? 120 : 420;

for (let i = 0; i < totalBrasas; i++) {
  const brasa = document.createElement('span');
  brasa.style.left = Math.random() * 100 + '%';
  brasa.style.top = Math.random() * 100 + '%';
  brasa.style.animationDelay = (Math.random() * 12) + 's';
  brasa.style.animationDuration = (8 + Math.random() * 8) + 's';
  brasa.style.width = brasa.style.height = (2 + Math.random() * 4) + 'px';

  brasa.addEventListener('mouseenter', () => {
    brasa.style.boxShadow = '0 0 10px #ff6a00, 0 0 20px #ff0000';
    brasa.style.transform = 'scale(2)';
  });

  brasa.addEventListener('mouseleave', () => {
    brasa.style.boxShadow = 'none';
    brasa.style.transform = 'scale(1)';
  });

  brasasContainer.appendChild(brasa);
}

// === Destellos energéticos en sección burn ===
const burnSection = document.querySelector('.slide.burn');
const totalDestellos = esMovil() ? 30 : 90;

for (let i = 0; i < totalDestellos; i++) {
  const destello = document.createElement('div');
  destello.className = 'destello';
  destello.style.left = Math.random() * 100 + '%';
  destello.style.top = Math.random() * 100 + '%';
  destello.style.animationDelay = (Math.random() * 3) + 's';
  destello.style.animationDuration = (1 + Math.random() * 2) + 's';
  destello.style.width = destello.style.height = (6 + Math.random() * 6) + 'px';
  destello.style.zIndex = 2;
  burnSection.appendChild(destello);
}
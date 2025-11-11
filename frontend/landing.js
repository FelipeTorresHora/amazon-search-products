// ============================================================================
// PARTICLES CANVAS
// ============================================================================

class ParticlesCanvas {
    constructor() {
        this.canvas = document.getElementById('particles');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: null, y: null, radius: 150 };

        this.init();
        this.animate();
        this.addEventListeners();
    }

    init() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;

        const numberOfParticles = window.innerWidth < 768 ? 50 : 100;

        for (let i = 0; i < numberOfParticles; i++) {
            const size = Math.random() * 3 + 1;
            const x = Math.random() * this.canvas.width;
            const y = Math.random() * this.canvas.height;
            const directionX = (Math.random() * 0.5) - 0.25;
            const directionY = (Math.random() * 0.5) - 0.25;
            const color = `rgba(102, 126, 234, ${Math.random() * 0.5 + 0.2})`;

            this.particles.push(new Particle(x, y, directionX, directionY, size, color, this.canvas));
        }
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        for (let i = 0; i < this.particles.length; i++) {
            this.particles[i].update(this.mouse);
            this.particles[i].draw(this.ctx);
        }

        this.connectParticles();
    }

    connectParticles() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 120) {
                    const opacity = (120 - distance) / 120 * 0.3;
                    this.ctx.strokeStyle = `rgba(102, 126, 234, ${opacity})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
    }

    addEventListeners() {
        window.addEventListener('resize', () => {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
        });

        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.x;
            this.mouse.y = e.y;
        });

        window.addEventListener('mouseout', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });
    }
}

class Particle {
    constructor(x, y, directionX, directionY, size, color, canvas) {
        this.x = x;
        this.y = y;
        this.directionX = directionX;
        this.directionY = directionY;
        this.size = size;
        this.color = color;
        this.canvas = canvas;
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    update(mouse) {
        if (this.x > this.canvas.width || this.x < 0) {
            this.directionX = -this.directionX;
        }
        if (this.y > this.canvas.height || this.y < 0) {
            this.directionY = -this.directionY;
        }

        // Mouse interaction
        if (mouse.x && mouse.y) {
            const dx = mouse.x - this.x;
            const dy = mouse.y - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < mouse.radius) {
                if (mouse.x < this.x && this.x < this.canvas.width - this.size * 10) {
                    this.x += 2;
                }
                if (mouse.x > this.x && this.x > this.size * 10) {
                    this.x -= 2;
                }
                if (mouse.y < this.y && this.y < this.canvas.height - this.size * 10) {
                    this.y += 2;
                }
                if (mouse.y > this.y && this.y > this.size * 10) {
                    this.y -= 2;
                }
            }
        }

        this.x += this.directionX;
        this.y += this.directionY;
    }
}

// Initialize particles
new ParticlesCanvas();

// ============================================================================
// NAVBAR SCROLL EFFECT
// ============================================================================

const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
});

// ============================================================================
// SMOOTH SCROLL
// ============================================================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));

        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============================================================================
// STATS COUNTER ANIMATION
// ============================================================================

class CountUp {
    constructor(element, target, duration = 2000) {
        this.element = element;
        this.target = target;
        this.duration = duration;
        this.startTime = null;
        this.started = false;
    }

    start() {
        if (this.started) return;
        this.started = true;
        this.startTime = null;
        this.animate();
    }

    animate(currentTime) {
        if (!this.startTime) this.startTime = currentTime;
        const progress = Math.min((currentTime - this.startTime) / this.duration, 1);

        const easeOutQuad = t => t * (2 - t);
        const currentNumber = Math.floor(this.target * easeOutQuad(progress));

        this.element.textContent = currentNumber.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame((time) => this.animate(time));
        }
    }
}

// Intersection Observer for stats
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = document.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const target = parseInt(stat.dataset.target);
                new CountUp(stat, target).start();
            });
            statsObserver.disconnect();
        }
    });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
    statsObserver.observe(heroStats);
}

// ============================================================================
// TILT EFFECT FOR CARDS
// ============================================================================

class TiltEffect {
    constructor(element) {
        this.element = element;
        this.init();
    }

    init() {
        this.element.addEventListener('mousemove', (e) => this.handleMove(e));
        this.element.addEventListener('mouseleave', () => this.handleLeave());
    }

    handleMove(e) {
        const rect = this.element.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        this.element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
    }

    handleLeave() {
        this.element.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
    }
}

// Apply tilt to feature cards
document.querySelectorAll('[data-tilt]').forEach(card => {
    new TiltEffect(card);
});

// ============================================================================
// FLOATING CARDS PARALLAX
// ============================================================================

window.addEventListener('mousemove', (e) => {
    const cards = document.querySelectorAll('.floating-card');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;

    cards.forEach((card, index) => {
        const speed = (index + 1) * 0.5;
        const x = (mouseX - 0.5) * speed * 20;
        const y = (mouseY - 0.5) * speed * 20;

        card.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// ============================================================================
// SCROLL REVEAL ANIMATION
// ============================================================================

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

// Apply reveal animation to sections
document.querySelectorAll('.feature-card, .pricing-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    revealObserver.observe(el);
});

// ============================================================================
// MOBILE MENU
// ============================================================================

const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navLinks = document.querySelector('.nav-links');
const navActions = document.querySelector('.nav-actions');

mobileMenuBtn?.addEventListener('click', () => {
    mobileMenuBtn.classList.toggle('active');
    navLinks?.classList.toggle('active');
    navActions?.classList.toggle('active');
});

// ============================================================================
// SPARKLINE ANIMATION
// ============================================================================

function drawSparkline() {
    const sparklines = document.querySelectorAll('.card-sparkline');

    sparklines.forEach(sparkline => {
        const canvas = document.createElement('canvas');
        canvas.width = 80;
        canvas.height = 30;
        sparkline.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        const data = Array.from({ length: 10 }, () => Math.random() * 20 + 5);

        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 2;
        ctx.beginPath();

        data.forEach((value, index) => {
            const x = (index / (data.length - 1)) * canvas.width;
            const y = canvas.height - (value / 30) * canvas.height;

            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();
    });
}

// Draw sparklines after DOM loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', drawSparkline);
} else {
    drawSparkline();
}

// ============================================================================
// CURSOR TRAIL EFFECT (OPTIONAL)
// ============================================================================

class CursorTrail {
    constructor() {
        this.dots = [];
        this.mouse = { x: 0, y: 0 };
        this.init();
    }

    init() {
        for (let i = 0; i < 12; i++) {
            const dot = document.createElement('div');
            dot.className = 'cursor-dot';
            dot.style.cssText = `
                position: fixed;
                width: ${20 - i}px;
                height: ${20 - i}px;
                background: rgba(102, 126, 234, ${0.6 - i * 0.05});
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                transition: all 0.1s ease;
            `;
            document.body.appendChild(dot);
            this.dots.push({ el: dot, x: 0, y: 0 });
        }

        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });

        this.animate();
    }

    animate() {
        let x = this.mouse.x;
        let y = this.mouse.y;

        this.dots.forEach((dot, index) => {
            dot.el.style.left = x - 10 + 'px';
            dot.el.style.top = y - 10 + 'px';

            const nextDot = this.dots[index + 1] || this.dots[0];
            dot.x = x;
            dot.y = y;

            x += (nextDot.x - dot.x) * 0.6;
            y += (nextDot.y - dot.y) * 0.6;
        });

        requestAnimationFrame(() => this.animate());
    }
}

// Enable cursor trail on desktop only
if (window.innerWidth > 1024) {
    // new CursorTrail(); // Uncomment to enable
}

// ============================================================================
// GRADIENT ANIMATION
// ============================================================================

const gradientElements = document.querySelectorAll('.gradient-text');

gradientElements.forEach(el => {
    let hue = 0;

    setInterval(() => {
        hue = (hue + 1) % 360;
        const color1 = `hsl(${hue}, 70%, 60%)`;
        const color2 = `hsl(${(hue + 60) % 360}, 70%, 60%)`;

        el.style.background = `linear-gradient(135deg, ${color1}, ${color2})`;
        el.style.webkitBackgroundClip = 'text';
        el.style.webkitTextFillColor = 'transparent';
        el.style.backgroundClip = 'text';
    }, 50);
});

// ============================================================================
// PERFORMANCE OPTIMIZATION
// ============================================================================

// Lazy load images
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            imageObserver.unobserve(img);
        }
    });
});

document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
});

// Debounce resize events
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        // Handle resize
        console.log('Resize completed');
    }, 250);
});

console.log('🚀 Landing page loaded successfully!');

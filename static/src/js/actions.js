
/*  */
/* Carousel Index */
const container = document.querySelector('.scroll-container');
const sections = document.querySelectorAll('.scroll-section');
const dots = document.querySelectorAll('.fixed.right-8 button');
let currentIndex = 0;
let autoScrollTimer;
let isManualScroll = false;

    // Inicialização
    function initCarousel() {
        // Ativa a primeira seção com animação
        setTimeout(() => {
            activateSection(0);
        }, 100);
        
        startAutoScroll();
        setupIntersectionObserver();
        setupEvents();
    }

    function activateSection(index) {
        // Remove classes ativas de todas as seções
        sections.forEach(section => {
            section.classList.remove('active');
            
            // Reseta as animações de texto
            const texts = section.querySelectorAll('.text-reveal');
            texts.forEach(text => {
                text.classList.remove('reveal');
            });
        });
        
        // Ativa a seção atual
        sections[index].classList.add('active');
        currentIndex = index;
        updateDots(index);
        
        // Dispara animação dos textos após a seção estar ativa
        setTimeout(() => {
            animateText(index);
        }, 300);
    }

    function animateText(index) {
        const texts = sections[index].querySelectorAll('.text-reveal');
        texts.forEach((text, i) => {
            // Delay escalonado para cada elemento de texto
            setTimeout(() => {
                text.classList.add('reveal');
            }, i * 200);
        });
    }

    function updateDots(index) {
        dots.forEach((dot, i) => {
            dot.classList.toggle('bg-white', i === index);
            dot.classList.toggle('bg-white/20', i !== index);
            dot.classList.toggle('scale-150', i === index);
        });
    }

    function scrollToSection(index) {
        if (index < 0 || index >= sections.length) return;

        isManualScroll = true;
        clearTimeout(autoScrollTimer);

        const offset = sections[index].offsetLeft;
        container.scrollTo({ left: offset, behavior: 'smooth' });

        setTimeout(() => {
            activateSection(index);
        }, 500);

        setTimeout(() => {
            isManualScroll = false;
            startAutoScroll();
        }, 5000);
    }

    function startAutoScroll() {
        if (isManualScroll) return;
        
        clearTimeout(autoScrollTimer);
        autoScrollTimer = setTimeout(() => {
            const nextIndex = (currentIndex + 1) % sections.length;
            scrollToSection(nextIndex);
        }, 5000);
    }

    function setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const newIndex = Array.from(sections).indexOf(entry.target);
                    if (newIndex !== -1 && newIndex !== currentIndex) {
                        currentIndex = newIndex;
                        activateSection(newIndex);
                        updateDots(newIndex);
                    }
                }
            });
        }, { threshold: 0.7 }); // Aumentei o threshold para 70%

        sections.forEach(section => observer.observe(section));
    }

    function setupEvents() {
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => scrollToSection(index));
        });
        
        container.addEventListener('wheel', () => {
            isManualScroll = true;
            clearTimeout(autoScrollTimer);
        });
        
        container.addEventListener('touchmove', () => {
            isManualScroll = true;
            clearTimeout(autoScrollTimer);
        });
        
        container.addEventListener('scrollend', () => {
            if (isManualScroll) {
                setTimeout(() => {
                    isManualScroll = false;
                    startAutoScroll();
                }, 5000);
            }
        });
    }

document.addEventListener('DOMContentLoaded', initCarousel);



/*  */
/* Back to top */
var toTopButton = document.getElementById("to-top-button");

    if (toTopButton) {

        window.onscroll = function() {
            if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
                toTopButton.classList.remove("hidden");
            } else {
                toTopButton.classList.add("hidden");
            }
        };

        window.goToTop = function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        };
    }



/*  */
/* Slide */
const slides = document.querySelector('.slides');
const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');

function updateSlider() {
    const slideWidth = slides.children[0].clientWidth;
    slides.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
}

prevButton.addEventListener('click', () => {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : slides.children.length - 1;
    updateSlider();
});

nextButton.addEventListener('click', () => {
    currentIndex = (currentIndex < slides.children.length - 1) ? currentIndex + 1 : 0;
    updateSlider();
});

window.addEventListener('resize', updateSlider);


/**  */
/* Modal */
document.getElementById("openModal").addEventListener("click", function() {
    document.getElementById("bidModal").classList.remove("hidden");
});

document.getElementById("closeModal").addEventListener("click", function() {
    document.getElementById("bidModal").classList.add("hidden");
});
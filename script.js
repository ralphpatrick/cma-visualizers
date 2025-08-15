// Year
(function setYear() {
	document.getElementById('year').textContent = String(new Date().getFullYear());
})();

// Mobile nav toggle
(function navToggle() {
	const toggle = document.querySelector('.nav-toggle');
	const menu = document.getElementById('nav-menu');
	if (!toggle || !menu) return;
	toggle.addEventListener('click', () => {
		const expanded = toggle.getAttribute('aria-expanded') === 'true';
		toggle.setAttribute('aria-expanded', String(!expanded));
		menu.classList.toggle('open');
		menu.style.display = menu.classList.contains('open') ? 'flex' : '';
	});
	menu.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
		toggle.setAttribute('aria-expanded', 'false');
		menu.classList.remove('open');
		menu.style.display = '';
	}));
})();

// Accordion
(function accordion() {
	const headers = Array.from(document.querySelectorAll('.accordion-header'));
	headers.forEach((btn) => {
		const panelId = btn.getAttribute('aria-controls');
		const panel = panelId ? document.getElementById(panelId) : null;
		if (!panel) return;
		btn.addEventListener('click', () => {
			const expanded = btn.getAttribute('aria-expanded') === 'true';
			btn.setAttribute('aria-expanded', String(!expanded));
			panel.hidden = expanded;
		});
		// ensure hidden matches initial state
		if (btn.getAttribute('aria-expanded') === 'true') {
			panel.hidden = false;
		}
	});
})();

// Testimonial carousel
(function carousel() {
	const track = document.querySelector('.carousel-track');
	const prev = document.querySelector('.carousel-prev');
	const next = document.querySelector('.carousel-next');
	const dotsWrap = document.querySelector('.carousel-dots');
	if (!track || !prev || !next || !dotsWrap) return;
	const slides = Array.from(track.children);
	let index = 0;
	let timer;

	function update() {
		const offset = -index * track.clientWidth;
		track.style.transform = `translateX(${offset}px)`;
		dotsWrap.querySelectorAll('button').forEach((b, i) => b.setAttribute('aria-selected', String(i === index)));
	}

	function go(to) {
		index = (to + slides.length) % slides.length;
		update();
	}

	// build dots
	slides.forEach((_, i) => {
		const b = document.createElement('button');
		b.type = 'button';
		b.setAttribute('role', 'tab');
		b.setAttribute('aria-label', `Go to testimonial ${i + 1}`);
		b.addEventListener('click', () => go(i));
		dotsWrap.appendChild(b);
	});
	update();

	prev.addEventListener('click', () => go(index - 1));
	next.addEventListener('click', () => go(index + 1));

	function start() { timer = window.setInterval(() => go(index + 1), 5000); }
	function stop() { window.clearInterval(timer); }

	const carousel = document.querySelector('.carousel');
	carousel.addEventListener('mouseenter', stop);
	carousel.addEventListener('mouseleave', start);
	carousel.addEventListener('focusin', stop);
	carousel.addEventListener('focusout', start);
	start();
	window.addEventListener('resize', update);
})();

// Email capture (demo only)
(function emailCapture() {
	const form = document.querySelector('.email-form');
	if (!form) return;
	form.addEventListener('submit', (e) => {
		e.preventDefault();
		const input = form.querySelector('input[type="email"]');
		if (!input) return;
		const value = String(input.value || '').trim();
		const ok = /.+@.+\..+/.test(value);
		if (!ok) {
			input.setAttribute('aria-invalid', 'true');
			input.focus();
			return;
		}
		input.setAttribute('aria-invalid', 'false');
		const msg = document.createElement('div');
		msg.textContent = 'Thanks! Check your inbox.';
		msg.style.marginTop = '8px';
		msg.style.color = '#1D6E4B';
		form.appendChild(msg);
		(/** clear */() => setTimeout(() => { try { form.reset(); } catch(_){} }, 100))();
	});
})();
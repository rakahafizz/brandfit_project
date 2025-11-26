/* main.js
   Smooth scroll, reveal on scroll, subtle card tilt, WA button helper.
   Keamanan kecil ditambahkan: semua initialisasi dijalankan saat DOM siap.
*/

document.addEventListener('DOMContentLoaded', () => {
  // 1) Smooth scrolling for internal anchors (works with fixed header)
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      // offset untuk fixed header (sesuaikan kalau perlu)
      const headerOffset = 88;
      const elementPosition = target.getBoundingClientRect().top + window.pageYOffset;
      const offsetPosition = elementPosition - headerOffset;
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    });
  });

  // 2) Reveal on scroll (IntersectionObserver)
  const revealSelector = ['.card', '.about-card', '.hero-content', '.product-container', '.product-details', '.product-image'];
  const revealEls = Array.from(document.querySelectorAll(revealSelector.join(',')));
  if (revealEls.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in');
          entry.target.classList.remove('opacity-zero');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    revealEls.forEach(el => {
      if (!el.classList.contains('fade-in')) {
        el.classList.add('opacity-zero');
        io.observe(el);
      }
    });
  } else {
    // fallback: show everything if IntersectionObserver tidak tersedia
    revealEls.forEach(el => el.classList.add('fade-in'));
  }

  // 3) Subtle 3D tilt effect on product cards (non-intrusive)
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.style.transition = 'transform .22s ease, box-shadow .22s ease';
    card.addEventListener('mousemove', (ev) => {
      const rect = card.getBoundingClientRect();
      const mx = (ev.clientX - rect.left) / rect.width; // 0..1
      const my = (ev.clientY - rect.top) / rect.height; // 0..1
      const rx = (my - 0.5) * 6; // rotateX
      const ry = (mx - 0.5) * -6; // rotateY
      card.style.transform = `perspective(800px) translateY(-6px) rotateX(${rx}deg) rotateY(${ry}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });

  // 4) Button hover micro-feedback for main CTA(s)
  document.querySelectorAll('.btn, .btn-small, .btn-wa').forEach(btn => {
    btn.addEventListener('mousedown', () => btn.style.transform = 'translateY(1px) scale(.998)');
    btn.addEventListener('mouseup', () => btn.style.transform = '');
    btn.addEventListener('mouseleave', () => btn.style.transform = '');
  });

  // 5) Safety: prevent links with href="#" from doing anything
  document.querySelectorAll('a').forEach(a => {
    if (a.getAttribute('href') === '#') {
      a.addEventListener('click', (e) => e.preventDefault());
    }
  });

  // 6) Auto-add "Chat WA" button when order success message present
  const messages = document.querySelectorAll('.alert-success, .messages .alert-success');
  if (messages.length) {
    messages.forEach(msg => {
      if (!msg.querySelector('.wa-inline-btn')) {
        const wa = document.createElement('a');
        const phone = '628389045852'; // <-- GANTI NOMOR DI SINI jika perlu (tanpa +)
        const productName = encodeURIComponent(document.title || 'pesanan');
        wa.href = `https://wa.me/${phone}?text=Halo,%20saya%20ingin%20melakukan%20pembayaran%20untuk%20${productName}`;
        wa.className = 'btn btn-wa wa-inline-btn';
        wa.style.marginLeft = '12px';
        wa.style.display = 'inline-block';
        wa.setAttribute('target', '_blank');
        wa.textContent = 'Chat WA';
        msg.appendChild(wa);
      }
    });
  }

  // 7) Small accessibility tweak: enable focus-visible style for keyboard users
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') document.body.classList.add('user-is-tabbing');
  });

  /* --- NAV TOGGLE (mobile) --- */
  const navToggleBtn = document.getElementById('nav-toggle');
  const mainNav = document.getElementById('main-nav');
  if (navToggleBtn && mainNav) {
    navToggleBtn.addEventListener('click', () => {
      const open = mainNav.classList.toggle('open');
      navToggleBtn.classList.toggle('open', open);
      navToggleBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    // close nav when clicking a link (mobile)
    mainNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mainNav.classList.remove('open');
        navToggleBtn.classList.remove('open');
        navToggleBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // 8) Disable submit button after click to prevent double submits
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', (e) => {
    if (!form.checkValidity()) {
      // show native HTML5 messages
      return;
    }
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.dataset.origText = btn.textContent;
      btn.textContent = 'Mengirim...';
    }
  });
});
})



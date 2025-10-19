/* main.js
   Smooth scroll, reveal on scroll, subtle card tilt, WA button helper.
   Meant to work with your CSS as-is; tidak mengubah tampilan.
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
      // compute offset to account for fixed header (approx 80px)
      const headerOffset = 88;
      const elementPosition = target.getBoundingClientRect().top + window.pageYOffset;
      const offsetPosition = elementPosition - headerOffset;
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    });
  });

  // 2) Reveal on scroll (IntersectionObserver) - elements: .card, .about-card, .hero-content, .product-container
  const revealSelector = ['.card', '.about-card', '.hero-content', '.product-container', '.product-details', '.product-image'];
  const revealEls = Array.from(document.querySelectorAll(revealSelector.join(',')));
  if (revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in');
          entry.target.classList.remove('opacity-zero');
          // optional: unobserve for performance
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

  // 5) Make any "Order" links to product detail open in same page anchor if slug/PK missing.
  //    (Graceful fallback: if product links are wrong, this prevents blank behaviour)
  document.querySelectorAll('a[href*="product/"]').forEach(a => {
    // if href endswith slash with non-numeric segment, do nothing here;
    // This is only a safety: if link is '#', ignore.
    if (a.getAttribute('href') === '#') {
      a.addEventListener('click', (e) => e.preventDefault());
    }
  });

  // 6) Optional: auto-add "Chat WA" button when order success message present
  //    (It looks for an element that has alert-success text and appends WA button near it)
  const messages = document.querySelectorAll('.alert-success, .messages .alert-success');
  if (messages.length) {
    messages.forEach(msg => {
      // avoid duplicating WA button
      if (!msg.querySelector('.wa-inline-btn')) {
        const wa = document.createElement('a');
        // change number/text as needed
        const phone = '628389045852';
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
});

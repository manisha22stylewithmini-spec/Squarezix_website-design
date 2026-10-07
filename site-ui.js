// Site-wide UI: the quick-contact dock (WhatsApp / email / LinkedIn) and the contact-us popup.
// Every [data-contact-open] button opens the popup; it validates, then hands off to the visitor's mail app
// (no form backend yet: swap the mailto for your form endpoint when one exists).
(() => {
  if (document.getElementById('zx-contact')) return;
  const WA = 'https://wa.me/971551318051?text=Hi%20SquareZix%2C%20I%27d%20like%20to%20talk%20about%20a%20project.';
  const ico = (d) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const waIco = ico('<path d="M20.5 11.6a8.5 8.5 0 0 1-12.6 7.4L3.5 20.5l1.6-4.2A8.5 8.5 0 1 1 20.5 11.6Z"/><path d="M9.2 8.6c.2-.5.6-.5.9-.4l.9 2.1c.1.3 0 .5-.2.8l-.6.7a6 6 0 0 0 2.8 2.8l.7-.7c.3-.3.5-.3.8-.2l2 .9c.3.2.4.6.2 1-.4 1-1.5 1.6-2.6 1.4-3-.6-5.5-3.1-6.1-6.1-.1-.9.2-1.7.5-2.3Z" fill="currentColor" stroke="none"/>');
  const mailIco = ico('<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3.8 7.2 8.2 6.2 8.2-6.2"/>');
  const liIco = ico('<rect x="3.5" y="3.5" width="17" height="17" rx="4"/><path d="M8 10.5V16M8 7.8v.01M11.5 16v-3a2 2 0 0 1 4 0v3M11.5 10.5V16"/>');
  const closeIco = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>';
  const phoneIco = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.18 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/><path d="M15 2.5a6 6 0 0 1 6.5 6.5M15 6a2.5 2.5 0 0 1 3 3"/></svg>';

  const root = document.createElement('div');
  root.innerHTML = `
    <nav class="qc" aria-label="Quick contact">
      <a class="qc-btn qc-btn--wa" href="${WA}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp"><span class="qc-ico">${waIco}</span><span class="qc-tip">Chat on WhatsApp</span></a>
      <a class="qc-btn qc-btn--mail" href="mailto:info@squarezix.com?subject=Project%20enquiry" aria-label="Email info@squarezix.com"><span class="qc-ico">${mailIco}</span><span class="qc-tip">Email us</span></a>
      <a class="qc-btn qc-btn--li" href="https://www.linkedin.com/company/squarezix-marketing-agency/" target="_blank" rel="noopener" aria-label="SquareZix on LinkedIn"><span class="qc-ico">${liIco}</span><span class="qc-tip">Connect on LinkedIn</span></a>
    </nav>
    <dialog class="zx-modal" id="zx-contact" aria-labelledby="zx-contact-title">
      <button type="button" class="zx-modal-x" data-contact-close aria-label="Close contact form">${closeIco}</button>
      <div class="zx-modal-body">
        <span class="svc-badge">Let’s Talk</span>
        <h2 id="zx-contact-title" class="zx-modal-title">Tell us about <em>your project</em></h2>
        <p class="zx-modal-sub">Share a few details and we’ll come back with a plan within five days.</p>
        <form class="ab-form zx-form" id="zx-form" novalidate>
          <label class="ab-field"><span>Your Name <b>*</b></span><input type="text" name="name" placeholder="Enter Your Name" autocomplete="name" required /></label>
          <label class="ab-field"><span>Your Email <b>*</b></span><input type="email" name="email" placeholder="Enter Your Email" autocomplete="email" required /></label>
          <label class="ab-field ab-field--full"><span>Your Phone Number <b>*</b></span><input type="tel" name="phone" placeholder="Enter Your Phone Number" autocomplete="tel" required /></label>
          <label class="ab-field ab-field--full"><span>Your Message</span><textarea name="message" rows="3" placeholder="Type Here"></textarea></label>
          <div class="ab-form-foot ab-field--full">
            <button type="submit" class="zx-btn">${phoneIco} Send message</button>
            <p class="ab-form-note" id="zx-form-note" role="status"></p>
          </div>
        </form>
        <p class="zx-modal-alt">Prefer chat? <a href="${WA}" target="_blank" rel="noopener">WhatsApp us</a> or write to <a href="mailto:info@squarezix.com">info@squarezix.com</a></p>
      </div>
    </dialog>`;
  while (root.firstChild) document.body.appendChild(root.firstChild);

  const modal = document.getElementById('zx-contact');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (typeof modal.showModal !== 'function') return;
  let opener = null;
  const open = (btn) => {
    opener = btn || null;
    modal.querySelectorAll('.is-invalid').forEach((f) => f.classList.remove('is-invalid'));
    const n = document.getElementById('zx-form-note');
    if (n) n.textContent = '';
    if (!modal.open) modal.showModal();
    setTimeout(() => modal.querySelector('input[name="name"]')?.focus(), 60);
  };
  const close = () => { if (modal.open) modal.close(); };

  // delegated, so buttons that scripts add later (filters, load-more…) work too
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-contact-open]');
    if (b) { e.preventDefault(); open(b); }
  });
  modal.querySelector('[data-contact-close]').addEventListener('click', close);
  modal.addEventListener('click', (e) => { if (e.target === modal) close(); });
  modal.addEventListener('close', () => opener?.focus?.());

  const form = document.getElementById('zx-form'), note = document.getElementById('zx-form-note');
  form.addEventListener('input', (e) => e.target.closest('.ab-field')?.classList.remove('is-invalid'));
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let ok = true;
    form.querySelectorAll('[required]').forEach((input) => {
      const bad = !input.value.trim() || (input.type === 'email' && !/^\S+@\S+\.\S+$/.test(input.value));
      input.closest('.ab-field').classList.toggle('is-invalid', bad);
      if (bad && ok) { input.focus(); ok = false; }
    });
    if (!ok) { note.textContent = 'Please fill in the required fields.'; return; }
    const d = Object.fromEntries(new FormData(form));
    const body = `Name: ${d.name}\nEmail: ${d.email}\nPhone: ${d.phone}\n\n${d.message || ''}`;
    window.location.href = `mailto:info@squarezix.com?subject=${encodeURIComponent(`New enquiry from ${d.name}`)}&body=${encodeURIComponent(body)}`;
    const done = document.createElement('div');
    done.className = 'zx-modal-done';
    done.innerHTML = '<b>Thank you!</b><span>Your email app is opening with your message. We’ll come back with a plan within five days.</span>';
    form.replaceWith(done);
  });
})();

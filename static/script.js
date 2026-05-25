/* ============================================================
   VolunteerHub — script.js
   Plain vanilla JS — no frameworks
   ============================================================ */

/* ── Confirm before delete ── */
function confirmDelete(type, name) {
  const label = name ? `"${name}"` : `this ${type}`;
  return confirm(`Delete ${label}?\n\nThis action cannot be undone.`);
}

/* Toggle password visibility on auth pages */
function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId || 'password');
  if (!input) return;

  if (input.type === 'password') {
    input.type = 'text';
    if (btn) btn.innerHTML = '<i data-lucide="eye-off"></i>';
  } else {
    input.type = 'password';
    if (btn) btn.innerHTML = '<i data-lucide="eye"></i>';
  }
  if (window.lucide) lucide.createIcons();
}

function initLucideIcons() {
  if (window.lucide) lucide.createIcons();
}

/* ── Auto-dismiss flash messages after 4 s ── */
function initFlashMessages() {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      el.style.opacity    = '0';
      el.style.transform  = 'translateY(-6px)';
      setTimeout(function () { el.remove(); }, 420);
    }, 4000);
  });
}

/* ── Mobile nav toggle ── */
function initNavToggle() {
  const toggle = document.getElementById('navToggle');
  const menu   = document.getElementById('navMenu');
  if (!toggle || !menu) return;

  toggle.addEventListener('click', function () {
    const open = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });

  /* Close menu when a link inside is clicked */
  menu.querySelectorAll('.nav-link, .btn-logout').forEach(function (link) {
    link.addEventListener('click', function () {
      menu.classList.remove('open');
    });
  });

  /* Close on outside click */
  document.addEventListener('click', function (e) {
    if (!toggle.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove('open');
    }
  });
}

/* ── Set today as default date on event form ── */
function initDateDefault() {
  const dateInput = document.getElementById('date');
  if (dateInput && !dateInput.value) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
  }
}

/* ── Highlight active row on hover (accessibility helper) ── */
function initTableRowFocus() {
  document.querySelectorAll('.table tbody tr').forEach(function (row) {
    row.setAttribute('tabindex', '0');
  });
}

function initRolePicker() {
  const radios = document.querySelectorAll('input[name="role"]');
  const volunteerFields = document.querySelectorAll('.volunteer-only');
  if (!radios.length) return;

  function syncRoleFields() {
    const selected = document.querySelector('input[name="role"]:checked');
    const showVolunteerFields = !selected || selected.value === 'volunteer';
    volunteerFields.forEach(function (field) {
      field.style.display = showVolunteerFields ? '' : 'none';
    });
  }

  radios.forEach(function (radio) {
    radio.addEventListener('change', syncRoleFields);
  });
  syncRoleFields();
}

/* ── Boot ── */
document.addEventListener('DOMContentLoaded', function () {
  initLucideIcons();
  initFlashMessages();
  initNavToggle();
  initDateDefault();
  initTableRowFocus();
  initRolePicker();
});

window.addEventListener('load', initLucideIcons);

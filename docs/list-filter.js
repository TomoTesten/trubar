document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('filter');
  const rows  = document.querySelectorAll('#law-table tbody tr');
  if (!input) return;
  input.addEventListener('input', function() {
    const q = this.value.toLowerCase();
    rows.forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
});

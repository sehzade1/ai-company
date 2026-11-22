function formatPrice(cents) {
  const sign = cents < 0 ? '-' : '';
  const absCents = Math.abs(cents);
  const lira = Math.floor(absCents / 100);
  const kurus = String(absCents % 100).padStart(2, '0');
  return sign + lira + '.' + kurus + ' TL';
}

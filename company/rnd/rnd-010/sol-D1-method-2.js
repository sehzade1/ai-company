function formatPrice(cents) {
  const sign = cents < 0 ? '-' : '';
  const absCents = Math.abs(cents);
  const lira = Math.floor(absCents / 100);
  const kurus = absCents % 100;
  return sign + lira + '.' + String(kurus).padStart(2, '0') + ' TL';
}

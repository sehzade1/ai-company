function formatPrice(cents) {
  const totalCents = Math.round(cents);
  const sign = totalCents < 0 ? '-' : '';
  const absCents = Math.abs(totalCents);
  const lira = Math.floor(absCents / 100);
  const kurus = String(absCents % 100).padStart(2, '0');
  return `${sign}${lira}.${kurus} TL`;
}

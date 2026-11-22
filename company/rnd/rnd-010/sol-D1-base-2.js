function formatPrice(cents) {
  const rounded = Math.round(cents);
  const sign = rounded < 0 ? '-' : '';
  const absCents = Math.abs(rounded);
  const lira = Math.floor(absCents / 100);
  const kurus = String(absCents % 100).padStart(2, '0');
  return `${sign}${lira}.${kurus} TL`;
}

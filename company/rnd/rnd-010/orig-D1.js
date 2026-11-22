function formatPrice(cents) {
  const lira = Math.floor(cents / 100);
  const kurus = cents % 100;
  return lira + "." + kurus + " TL";
}
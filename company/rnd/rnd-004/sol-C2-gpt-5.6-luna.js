function parseDuration(str) {
  if (typeof str !== "string" || !str.trim()) {
    throw new Error("Invalid duration");
  }

  const input = str.trim();
  const numberPattern = String.raw`\d+(?:\.\d+)?`;

  if (new RegExp(`^${numberPattern}$`).test(input)) {
    const seconds = Number(input);
    if (!Number.isFinite(seconds)) throw new Error("Invalid duration");
    return seconds;
  }

  const tokenPattern = new RegExp(
    String.raw`\s*(${numberPattern})\s*([hms])`,
    "gi"
  );

  let position = 0;
  let lastUnit = -1;
  let total = 0;
  let match;

  while ((match = tokenPattern.exec(input)) !== null) {
    if (match.index !== position) {
      throw new Error("Invalid duration");
    }

    const value = Number(match[1]);
    const unit = match[2].toLowerCase();
    const order = { h: 0, m: 1, s: 2 }[unit];

    if (!Number.isFinite(value) || order <= lastUnit) {
      throw new Error("Invalid duration");
    }

    total += value * { h: 3600, m: 60, s: 1 }[unit];
    lastUnit = order;
    position = tokenPattern.lastIndex;
  }

  if (position !== input.length || !match || !Number.isFinite(total)) {
    throw new Error("Invalid duration");
  }

  return total;
}


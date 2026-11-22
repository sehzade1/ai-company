function parseDuration(str) {
  if (typeof str !== "string") throw new Error("Invalid duration");

  const input = str.trim();
  if (!input) throw new Error("Invalid duration");

  if (/^\d+(?:\.\d+)?$/.test(input)) return Number(input);

  const units = { h: 3600, m: 60, s: 1 };
  const order = { h: 3, m: 2, s: 1 };
  const pattern = /(\d+(?:\.\d+)?)([hms])/iy;
  let index = 0;
  let previousOrder = Infinity;
  let total = 0;

  while (index < input.length) {
    while (/\s/.test(input[index])) index++;
    if (index >= input.length) break;

    pattern.lastIndex = index;
    const match = pattern.exec(input);
    if (!match) throw new Error("Invalid duration");

    const unit = match[2].toLowerCase();
    if (order[unit] >= previousOrder) throw new Error("Invalid duration");

    total += Number(match[1]) * units[unit];
    previousOrder = order[unit];
    index = pattern.lastIndex;
  }

  return total;
}


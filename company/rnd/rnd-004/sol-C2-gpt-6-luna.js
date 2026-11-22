function parseDuration(str) {
  if (typeof str !== "string") {
    throw new Error("Duration must be a string");
  }

  const input = str.trim();
  if (input === "") {
    throw new Error("Duration cannot be empty");
  }

  if (/^\d+(?:\.\d+)?$/.test(input)) {
    return Number(input);
  }

  const partPattern = /(\d+(?:\.\d+)?)\s*([hms])/igy;
  let position = 0;
  let total = 0;
  let previousUnitOrder = -1;
  let matchedAny = false;
  const unitOrder = { h: 0, m: 1, s: 2 };
  const unitSeconds = { h: 3600, m: 60, s: 1 };

  while (position < input.length) {
    while (position < input.length && /\s/.test(input[position])) {
      position++;
    }

    partPattern.lastIndex = position;
    const match = partPattern.exec(input);
    if (!match) {
      throw new Error("Invalid duration");
    }

    const value = Number(match[1]);
    const unit = match[2].toLowerCase();
    const order = unitOrder[unit];

    if (order <= previousUnitOrder) {
      throw new Error("Duration units must be unique and in h, m, s order");
    }

    total += value * unitSeconds[unit];
    previousUnitOrder = order;
    position = partPattern.lastIndex;
    matchedAny = true;

    if (position < input.length && !/\s/.test(input[position]) && !/\d/.test(input[position])) {
      throw new Error("Invalid duration");
    }
  }

  if (!matchedAny) {
    throw new Error("Invalid duration");
  }

  return total;
}


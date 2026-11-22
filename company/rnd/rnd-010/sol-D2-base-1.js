function memoize(fn) {
  const cache = new Map();
  const RESULT = Symbol('result');

  return function (...args) {
    let node = cache;
    let hit = true;

    for (const arg of args) {
      if (!node.has(arg)) {
        hit = false;
        break;
      }
      node = node.get(arg);
    }

    if (hit && node.has(RESULT)) {
      return node.get(RESULT);
    }

    const result = fn.apply(this, args);

    node = cache;
    for (const arg of args) {
      let next = node.get(arg);
      if (!next) {
        next = new Map();
        node.set(arg, next);
      }
      node = next;
    }
    node.set(RESULT, result);

    return result;
  };
}

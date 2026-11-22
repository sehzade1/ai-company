function memoize(fn) {
  const RESULT = Symbol('result');
  const cache = new Map();

  return function (...args) {
    let node = cache;
    for (const arg of args) {
      if (!node.has(arg)) {
        node = undefined;
        break;
      }
      node = node.get(arg);
    }
    if (node && node.has(RESULT)) return node.get(RESULT);

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

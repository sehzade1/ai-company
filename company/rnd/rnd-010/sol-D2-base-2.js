function memoize(fn) {
  const cache = new Map();
  const RESULT = Symbol('result');

  return function (...args) {
    let node = cache;
    for (const arg of args) {
      let next = node.get(arg);
      if (!next) {
        next = new Map();
        node.set(arg, next);
      }
      node = next;
    }
    if (node.has(RESULT)) return node.get(RESULT);
    const result = fn.apply(this, args);
    node.set(RESULT, result);
    return result;
  };
}

function memoize(fn) {
  const RESULT = Symbol('result');
  const cache = new Map();

  return function (...args) {
    let node = cache;
    for (let i = 0; i < args.length; i++) {
      node = node?.get(args[i]);
    }
    if (node?.has(RESULT)) return node.get(RESULT);

    const result = fn(...args);
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

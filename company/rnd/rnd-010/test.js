// usage: node test.js D1|D2 solution.js
const fs = require('fs'), vm = require('vm');
const [task, file] = process.argv.slice(2);
const ctx = {}; vm.createContext(ctx);
try { vm.runInContext(fs.readFileSync(file, 'utf8') + '\n;globalThis.__f = (typeof formatPrice!=="undefined"?formatPrice:undefined); globalThis.__m = (typeof memoize!=="undefined"?memoize:undefined);', ctx); } catch (e) { console.log('LOAD_FAIL ' + e.message); process.exit(0); }
let pass = 0, total = 0, fails = [];
const check = (name, fn) => { total++; try { if (fn()) pass++; else fails.push(name); } catch (e) { fails.push(name + ' threw'); } };
if (task === 'D1') {
  const f = ctx.__f;
  for (const [i, o] of [[1005,'10.05 TL'],[0,'0.00 TL'],[99,'0.99 TL'],[7,'0.07 TL'],[100000,'1000.00 TL'],[-1005,'-10.05 TL'],[-5,'-0.05 TL']]) check(`${i}->${o}`, () => f(i) === o);
} else {
  const memoize = ctx.__m;
  check('1,2 vs "1,2"', () => { const f = memoize((...a) => JSON.stringify(a)); return f(1,2) === '[1,2]' && f('1,2') === '["1,2"]'; });
  check('null vs undefined', () => { const f = memoize(x => x === undefined ? 'U' : 'N'); return f(null) === 'N' && f(undefined) === 'U'; });
  check('"a" vs ["a"]', () => { const f = memoize(x => Array.isArray(x) ? 'arr' : 'str'); return f('a') === 'str' && f(['a']) === 'arr'; });
  check('caches repeated call', () => { let n = 0; const f = memoize((a,b) => { n++; return a+b; }); f(1,2); f(1,2); return n === 1; });
  check('caches falsy result', () => { let n = 0; const f = memoize(() => { n++; return 0; }); f(); f(); return n === 1; });
  check('key "constructor"', () => { const f = memoize(x => 'v:' + x); return f('constructor') === 'v:constructor'; });
  check('keeps this', () => { const o = { base: 10, m: memoize(function (x) { return this.base + x; }) }; return o.m(1) === 11; });
}
console.log(`PASS ${pass}/${total}` + (fails.length ? ' FAILS: ' + fails.join(' | ') : ''));
// usage: node test-c2.js solution.js
const fs = require('fs'); const vm = require('vm');
const src = fs.readFileSync(process.argv[2], 'utf8');
const ctx = {}; vm.createContext(ctx); try { vm.runInContext(src + '\n;globalThis.__f = parseDuration;', ctx); } catch (e) { console.log('LOAD_FAIL', e.message); process.exit(0); }
const f = ctx.__f;
const ok = [['1h30m',5400],['45s',45],['2h',7200],['1h 5m 10s',3910],['90',90],['1.5h',5400],['  10M ',600],['1H2S',3602],['0s',0],['2m30s',150]];
const bad = ['', '   ', '5x', '1h2h', '5m1h', '-5s', 'abc', '1h30', 'h', '1..5h', '5 s s'];
let pass = 0, total = ok.length + bad.length, fails = [];
for (const [i, e] of ok) { try { const r = f(i); if (Math.abs(r - e) < 1e-9) pass++; else fails.push(`${JSON.stringify(i)} -> ${r} (want ${e})`); } catch (x) { fails.push(`${JSON.stringify(i)} threw`); } }
for (const i of bad) { try { const r = f(i); fails.push(`${JSON.stringify(i)} -> ${r} (want throw)`); } catch (x) { pass++; } }
console.log(`PASS ${pass}/${total}`); if (fails.length) console.log('FAILS: ' + fails.join(' | '));

C1 answer key (6 bugs): 1) filter uses assignment u.active = true -> mutates input and keeps all; use u.active === true / u.active. 2) sort comparator returns boolean; use a.age - b.age. 3) page is 1-based: start = (page-1)*pageSize. 4) slice end off by one: start + pageSize. 5) reduce has no initial value (first element is an object) -> add 0. 6) empty list divides by zero -> NaN; must return 0. 7) pages uses Math.floor; must be Math.ceil.
Note: items 5 and 6 are separate defects -> 7 total.
A1 key: Q1 11325; Q2 Espresso (4510 vs Filter 4505); Q3 1785; Q4 Apr, 60; Q5 82.00

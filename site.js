/* Centered finite-difference dispersion; see dynamics_study/study.py. */
(() => {
  const range = document.getElementById('range');
  const grid = document.getElementById('chart-grid');
  const ns = 'http://www.w3.org/2000/svg';
  function element(tag, attributes, text) {
    const node = document.createElementNS(ns, tag);
    Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
    if (text !== undefined) node.textContent = text;
    grid.appendChild(node);
  }
  for (let i = 0; i <= 4; i++) {
    const y = 280 - 240 * i / 4;
    element('line', {x1:64, x2:850, y1:y, y2:y, stroke:'#e8eee8', opacity:0.1});
    element('text', {x:50, y:y + 5, 'text-anchor':'end', fill:'#a8b3ad', 'font-size':14}, (i / 4).toFixed(2));
    const x = 64 + 786 * i / 4;
    element('text', {x, y:306, 'text-anchor':'middle', fill:'#a8b3ad', 'font-size':14}, ['0','π/4','π/2','3π/4','π'][i]);
  }
  element('text', {x:70, y:22, fill:'#a8b3ad', 'font-size':14}, 'group speed / c');
  element('text', {x:455, y:329, 'text-anchor':'middle', fill:'#a8b3ad', 'font-size':14}, 'wave number × spacing (qk)');
  function coefficients(r) {
    const b = [0, 4];
    // b_m / b_(m-1) = 2(m-1)^2 / (m(2m-1)).
    for (let m = 2; m <= r; m++) b[m] = b[m-1] * 2 * (m-1)**2 / (m * (2*m-1));
    return b;
  }
  function speed(x, b) {
    if (x < 1e-10) return 1;
    const y = Math.sin(x/2)**2;
    let p = 0, derivative = 0;
    for (let m = 1; m < b.length; m++) {
      p += b[m] * y**m;
      derivative += m * b[m] * y**(m-1);
    }
    return derivative * Math.sin(x) / (4 * Math.sqrt(p));
  }
  function path(b) {
    return Array.from({length:501}, (_, i) => {
      const x = Math.PI * i / 500;
      return `${i ? 'L' : 'M'}${(64 + 786*i/500).toFixed(2)},${(280 - 240*speed(x,b)).toFixed(2)}`;
    }).join(' ');
  }
  document.getElementById('nearest').setAttribute('d', path(coefficients(1)));
  function update() {
    const r = Number(range.value), b = coefficients(r);
    document.getElementById('range-value').value = r;
    document.getElementById('legend-range').textContent = r;
    document.getElementById('centered').setAttribute('d', path(b));
    const error = 100 * (1-speed(Math.PI/2,b));
    document.getElementById('speed-summary').textContent = `Range ${r}: group-speed error at qk = π/2 (wavelength 4k) is ${error < 0.001 ? error.toPrecision(3) : error.toFixed(2)}%. The lattice spacing is unchanged.`;
  }
  range.addEventListener('input', update);
  update();
})();

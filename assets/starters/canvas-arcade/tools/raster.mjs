// Canvas de software só para amostrar o que o draw() pintou.
// Sem anti-alias, sem glifo: fillText vira retângulo da cor. Não é o compositor
// do navegador nem o dispositivo.

export function parseColor(style) {
  const value = String(style ?? "").trim();
  const hex = /^#([0-9a-f]{6})$/i.exec(value);
  if (hex) {
    const n = Number.parseInt(hex[1], 16);
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: 1 };
  }
  const rgb = /^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*,\s*([\d.]+))?\s*\)$/i.exec(value);
  if (!rgb) return null;
  return {
    r: Number(rgb[1]),
    g: Number(rgb[2]),
    b: Number(rgb[3]),
    a: rgb[4] === undefined ? 1 : Number(rgb[4]),
  };
}

export function createRasterCanvas(width, height) {
  const pixels = new Uint8ClampedArray(width * height * 4);
  let transform = { a: 1, d: 1, e: 0, f: 0 };
  let path = [];
  let font = "8px system-ui";
  let align = "left";

  const map = (x, y) => ({
    x: transform.a * x + transform.e,
    y: transform.d * y + transform.f,
  });

  const blend = (px, py, r, g, b, a) => {
    if (px < 0 || py < 0 || px >= width || py >= height || a <= 0) return;
    const index = (py * width + px) * 4;
    const destA = pixels[index + 3] / 255;
    const outA = a + destA * (1 - a);
    if (outA <= 0) return;
    pixels[index] = (r * a + pixels[index] * destA * (1 - a)) / outA;
    pixels[index + 1] = (g * a + pixels[index + 1] * destA * (1 - a)) / outA;
    pixels[index + 2] = (b * a + pixels[index + 2] * destA * (1 - a)) / outA;
    pixels[index + 3] = outA * 255;
  };

  const paint = (px, py, color, alpha) => {
    if (!color) return;
    blend(px, py, color.r, color.g, color.b, color.a * alpha);
  };

  const fillBox = (x0, y0, x1, y1, color, alpha) => {
    const left = Math.floor(Math.min(x0, x1));
    const right = Math.ceil(Math.max(x0, x1));
    const top = Math.floor(Math.min(y0, y1));
    const bottom = Math.ceil(Math.max(y0, y1));
    for (let py = top; py < bottom; py += 1) {
      for (let px = left; px < right; px += 1) paint(px, py, color, alpha);
    }
  };

  const fillCircle = (cx, cy, radius, color, alpha) => {
    const r = Math.max(0, radius);
    const left = Math.floor(cx - r);
    const right = Math.ceil(cx + r);
    const top = Math.floor(cy - r);
    const bottom = Math.ceil(cy + r);
    const r2 = r * r;
    for (let py = top; py < bottom; py += 1) {
      for (let px = left; px < right; px += 1) {
        const dx = px + 0.5 - cx;
        const dy = py + 0.5 - cy;
        if (dx * dx + dy * dy <= r2) paint(px, py, color, alpha);
      }
    }
  };

  const fillTriangle = (ax, ay, bx, by, cx, cy, color, alpha) => {
    const left = Math.floor(Math.min(ax, bx, cx));
    const right = Math.ceil(Math.max(ax, bx, cx));
    const top = Math.floor(Math.min(ay, by, cy));
    const bottom = Math.ceil(Math.max(ay, by, cy));
    const area = (bx - ax) * (cy - ay) - (cx - ax) * (by - ay);
    if (area === 0) return;
    for (let py = top; py < bottom; py += 1) {
      for (let px = left; px < right; px += 1) {
        const x = px + 0.5;
        const y = py + 0.5;
        const w0 = (bx - x) * (cy - y) - (cx - x) * (by - y);
        const w1 = (cx - x) * (ay - y) - (ax - x) * (cy - y);
        const w2 = (ax - x) * (by - y) - (bx - x) * (ay - y);
        if (w0 * area >= 0 && w1 * area >= 0 && w2 * area >= 0) paint(px, py, color, alpha);
      }
    }
  };

  const strokeBox = (x, y, w, h, color, alpha, lineWidth) => {
    const pad = Math.max(1, Math.round(lineWidth));
    fillBox(x, y, x + w, y + pad, color, alpha);
    fillBox(x, y + h - pad, x + w, y + h, color, alpha);
    fillBox(x, y, x + pad, y + h, color, alpha);
    fillBox(x + w - pad, y, x + w, y + h, color, alpha);
  };

  const points = () => {
    const mapped = [];
    for (const item of path) {
      if (item.kind === "arc" || item.kind === "rect") mapped.push(item);
      else mapped.push({ ...item, ...map(item.x, item.y) });
    }
    return mapped;
  };

  const context = {
    fillStyle: "#000000",
    strokeStyle: "#000000",
    lineWidth: 1,
    globalAlpha: 1,
    textBaseline: "top",
    setTransform(a, _b, _c, d, e, f) {
      transform = { a, d, e, f };
    },
    beginPath() {
      path = [];
    },
    closePath() {
      path.push({ kind: "close" });
    },
    moveTo(x, y) {
      path.push({ kind: "move", x, y });
    },
    lineTo(x, y) {
      path.push({ kind: "line", x, y });
    },
    arc(x, y, radius) {
      const center = map(x, y);
      path.push({ kind: "arc", x: center.x, y: center.y, radius: Math.abs(transform.a) * radius });
    },
    roundRect(x, y, w, h) {
      const origin = map(x, y);
      path.push({
        kind: "rect",
        x: origin.x,
        y: origin.y,
        width: Math.abs(transform.a) * w,
        height: Math.abs(transform.d) * h,
      });
    },
    fillRect(x, y, w, h) {
      const origin = map(x, y);
      fillBox(
        origin.x,
        origin.y,
        origin.x + Math.abs(transform.a) * w,
        origin.y + Math.abs(transform.d) * h,
        parseColor(context.fillStyle),
        context.globalAlpha,
      );
    },
    strokeRect(x, y, w, h) {
      const origin = map(x, y);
      strokeBox(
        origin.x,
        origin.y,
        Math.abs(transform.a) * w,
        Math.abs(transform.d) * h,
        parseColor(context.strokeStyle),
        context.globalAlpha,
        context.lineWidth * Math.abs(transform.a),
      );
    },
    fill() {
      const color = parseColor(context.fillStyle);
      const alpha = context.globalAlpha;
      const items = points();
      const arc = items.find((item) => item.kind === "arc");
      const rect = items.find((item) => item.kind === "rect");
      const verts = items.filter((item) => item.kind === "move" || item.kind === "line");
      if (arc) fillCircle(arc.x, arc.y, arc.radius, color, alpha);
      else if (rect) fillBox(rect.x, rect.y, rect.x + rect.width, rect.y + rect.height, color, alpha);
      else if (verts.length >= 3) {
        fillTriangle(verts[0].x, verts[0].y, verts[1].x, verts[1].y, verts[2].x, verts[2].y, color, alpha);
      }
      path = [];
    },
    stroke() {
      const color = parseColor(context.strokeStyle);
      const alpha = context.globalAlpha;
      const items = points();
      const arc = items.find((item) => item.kind === "arc");
      const rect = items.find((item) => item.kind === "rect");
      if (arc) {
        const inner = Math.max(0, arc.radius - context.lineWidth / 2);
        const outer = arc.radius + context.lineWidth / 2;
        const left = Math.floor(arc.x - outer);
        const right = Math.ceil(arc.x + outer);
        const top = Math.floor(arc.y - outer);
        const bottom = Math.ceil(arc.y + outer);
        for (let py = top; py < bottom; py += 1) {
          for (let px = left; px < right; px += 1) {
            const dx = px + 0.5 - arc.x;
            const dy = py + 0.5 - arc.y;
            const d2 = dx * dx + dy * dy;
            if (d2 <= outer * outer && d2 >= inner * inner) paint(px, py, color, alpha);
          }
        }
      } else if (rect) {
        strokeBox(rect.x, rect.y, rect.width, rect.height, color, alpha, context.lineWidth);
      }
      path = [];
    },
    measureText(text) {
      const size = Number.parseFloat(font) || 8;
      return { width: String(text).length * size * 0.62 };
    },
    fillText(text, x, y) {
      const size = Number.parseFloat(font) || 8;
      const width = context.measureText(text).width;
      const origin = map(align === "right" ? x - width : x, y);
      fillBox(
        origin.x,
        origin.y,
        origin.x + Math.abs(transform.a) * width,
        origin.y + Math.abs(transform.d) * size,
        parseColor(context.fillStyle),
        context.globalAlpha,
      );
    },
    set font(value) {
      font = value;
    },
    get font() {
      return font;
    },
    set textAlign(value) {
      align = value;
    },
    get textAlign() {
      return align;
    },
    save() {},
    restore() {},
    clearRect() {},
    rect() {},
    ellipse() {},
    quadraticCurveTo() {},
    createLinearGradient: () => ({ addColorStop() {} }),
    createRadialGradient: () => ({ addColorStop() {} }),
  };

  return {
    width,
    height,
    style: {},
    pixels,
    getContext: () => context,
    sample(x, y) {
      const point = map(x, y);
      const px = Math.floor(point.x);
      const py = Math.floor(point.y);
      if (px < 0 || py < 0 || px >= width || py >= height) return null;
      const index = (py * width + px) * 4;
      return {
        r: pixels[index],
        g: pixels[index + 1],
        b: pixels[index + 2],
        a: Number((pixels[index + 3] / 255).toFixed(3)),
      };
    },
  };
}

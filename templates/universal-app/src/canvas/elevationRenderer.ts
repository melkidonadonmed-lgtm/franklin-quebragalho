import { ElevationCanvasOptions, ElevationLevel } from '../types';

interface ShadowLayerSpec {
  offsetY: number;
  blur: number;
  spreadInset: number;
  color: string;
}

interface ElevationSpec {
  ambientPenumbra: ShadowLayerSpec;
  contactUmbra: ShadowLayerSpec;
  topCatchLightAlpha: number;
  isRecessed?: boolean;
}

/**
 * Tabela canônica dos 3 Níveis de Sombras Multi-Camadas + Sunken (SSOT Eixo 5):
 * - Camada 1 (Penumbra Difusa / Key Light): blur amplo + spread negativo (simulado por inset de geometria)
 *   para conter vazamento lateral e projetar luz zenital (90°–120°).
 * - Camada 2 (Umbra de Contato / Oclusão): blur curto (2px–6px) ancorando o componente no canvas.
 * - Camada 3 (Luz Zenital + Anel Perimetral 1px): reflexo especular superior (`inset 0 1px 0 0`) +
 *   contorno de 1px em `oklch()`.
 */
const ELEVATION_SPECS: Record<ElevationLevel, ElevationSpec> = {
  sunken: {
    ambientPenumbra: { offsetY: 2, blur: 4, spreadInset: 0, color: 'oklch(0.10 0.02 255 / 0.42)' },
    contactUmbra: { offsetY: 1, blur: 2, spreadInset: 0, color: 'oklch(0.10 0.02 255 / 0.28)' },
    topCatchLightAlpha: 0.06,
    isRecessed: true,
  },
  flat: {
    ambientPenumbra: { offsetY: 0, blur: 0, spreadInset: 0, color: 'oklch(0.12 0.02 255 / 0)' },
    contactUmbra: { offsetY: 0, blur: 0, spreadInset: 0, color: 'oklch(0.12 0.02 255 / 0)' },
    topCatchLightAlpha: 0.08,
  },
  'elevation-1': {
    ambientPenumbra: { offsetY: 2, blur: 6, spreadInset: 1, color: 'oklch(0.12 0.02 255 / 0.14)' },
    contactUmbra: { offsetY: 1, blur: 2, spreadInset: 0, color: 'oklch(0.12 0.02 255 / 0.22)' },
    topCatchLightAlpha: 0.12,
  },
  card: {
    ambientPenumbra: { offsetY: 2, blur: 6, spreadInset: 1, color: 'oklch(0.12 0.02 255 / 0.14)' },
    contactUmbra: { offsetY: 1, blur: 2, spreadInset: 0, color: 'oklch(0.12 0.02 255 / 0.22)' },
    topCatchLightAlpha: 0.12,
  },
  'elevation-2': {
    ambientPenumbra: { offsetY: 8, blur: 18, spreadInset: 2, color: 'oklch(0.12 0.02 255 / 0.26)' },
    contactUmbra: { offsetY: 2, blur: 5, spreadInset: 1, color: 'oklch(0.12 0.02 255 / 0.32)' },
    topCatchLightAlpha: 0.16,
  },
  raised: {
    ambientPenumbra: { offsetY: 8, blur: 18, spreadInset: 2, color: 'oklch(0.12 0.02 255 / 0.26)' },
    contactUmbra: { offsetY: 2, blur: 5, spreadInset: 1, color: 'oklch(0.12 0.02 255 / 0.32)' },
    topCatchLightAlpha: 0.16,
  },
  'elevation-3': {
    ambientPenumbra: { offsetY: 20, blur: 36, spreadInset: 4, color: 'oklch(0.10 0.02 255 / 0.44)' },
    contactUmbra: { offsetY: 6, blur: 12, spreadInset: 2, color: 'oklch(0.10 0.02 255 / 0.36)' },
    topCatchLightAlpha: 0.22,
  },
};

/**
 * Renderizador de Elevação Física Multi-Camadas em 3 Níveis (SSOT Eixo 5) para HTML5 Canvas 2D:
 * 1. Passagem 1 (Penumbra Difusa com compensação de spread negativo): projeta profundidade direcional
 *    sem vazar nas laterais.
 * 2. Passagem 2 (Umbra de Contato): oclusão curta e nítida na base do cartão + preenchimento da superfície.
 * 3. Passagem 3 (Anel Perimetral 1px + Luz Zenital Superior `inset 0 1px 0 0`): garante recorte óptico
 *    em Dark Mode (`L = 0.16 -> 0.22 -> 0.27`) e Light Mode.
 */
export function drawElevatedCard(
  ctx: CanvasRenderingContext2D,
  options: ElevationCanvasOptions
): void {
  const {
    x,
    y,
    width,
    height,
    radius,
    fillColor,
    rimColor = 'oklch(0.98 0.005 255 / 0.08)',
    topHighlightColor,
    elevation = 'elevation-1',
  } = options;

  const spec = ELEVATION_SPECS[elevation] ?? ELEVATION_SPECS['elevation-1'];

  ctx.save();

  if (!spec.isRecessed && spec.ambientPenumbra.blur > 0) {
    // Passagem 1: Penumbra Difusa com compensação geométrica de spread negativo
    const inset = spec.ambientPenumbra.spreadInset;
    ctx.shadowColor = spec.ambientPenumbra.color;
    ctx.shadowBlur = spec.ambientPenumbra.blur;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = spec.ambientPenumbra.offsetY;
    drawRoundedPath(
      ctx,
      x + inset,
      y + inset,
      Math.max(1, width - inset * 2),
      Math.max(1, height - inset * 2),
      Math.max(0, radius - inset)
    );
    ctx.fillStyle = fillColor;
    ctx.fill();
  }

  // Passagem 2: Umbra de Contato (Oclusão curta) + Preenchimento principal da superfície
  if (!spec.isRecessed && spec.contactUmbra.blur > 0) {
    ctx.shadowColor = spec.contactUmbra.color;
    ctx.shadowBlur = spec.contactUmbra.blur;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = spec.contactUmbra.offsetY;
  } else {
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;
  }
  drawRoundedPath(ctx, x, y, width, height, radius);
  ctx.fillStyle = fillColor;
  ctx.fill();
  ctx.restore();

  // Caso Sunken (Recesso Tátil Interno): desenha sombra interna no topo após clipar a geometria
  if (spec.isRecessed) {
    ctx.save();
    drawRoundedPath(ctx, x, y, width, height, radius);
    ctx.clip();
    ctx.strokeStyle = spec.ambientPenumbra.color;
    ctx.lineWidth = 2;
    ctx.shadowColor = spec.contactUmbra.color;
    ctx.shadowBlur = spec.ambientPenumbra.blur;
    ctx.shadowOffsetY = spec.ambientPenumbra.offsetY;
    drawRoundedPath(ctx, x, y - 1, width, height + 2, radius);
    ctx.stroke();
    ctx.restore();
  }

  // Passagem 3: Anel Perimetral de 1px + Luz Zenital de Topo (inset 0 1px 0 0)
  ctx.save();
  drawRoundedPath(ctx, x + 0.5, y + 0.5, width - 1, height - 1, radius);
  ctx.lineWidth = 1;
  ctx.strokeStyle = rimColor;
  ctx.stroke();

  if (width > radius * 2) {
    const catchY = spec.isRecessed ? y + height - 0.5 : y + 0.5;
    ctx.beginPath();
    ctx.moveTo(x + radius, catchY);
    ctx.lineTo(x + width - radius, catchY);
    ctx.strokeStyle =
      topHighlightColor ?? `oklch(0.99 0.002 255 / ${spec.topCatchLightAlpha})`;
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  ctx.restore();
}

/**
 * Caminho arredondado compatível com CanvasRenderingContext2D moderno (`roundRect`) e fallback quadrático.
 */
function drawRoundedPath(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number
): void {
  ctx.beginPath();
  if (typeof ctx.roundRect === 'function') {
    ctx.roundRect(x, y, w, h, r);
  } else {
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
  }
  ctx.closePath();
}

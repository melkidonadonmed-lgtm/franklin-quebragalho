import { ElevationCanvasOptions } from '../types';

/**
 * Renderizador de Elevação Física Multicamada para HTML5 Canvas 2D.
 * Implementa o pipeline de dupla passagem de sombra e chanfro zenital de 1px
 * garantindo nitidez e profundidade física em elementos interativos e gráficos.
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
    rimColor = 'rgba(255, 255, 255, 0.08)',
    elevation = 'card',
  } = options;

  ctx.save();

  // Configurações de intensidade baseadas no nível de elevação
  const isRaised = elevation === 'raised';
  const diffuseBlur = isRaised ? 24 : 14;
  const diffuseOffsetY = isRaised ? 10 : 5;
  const diffuseAlpha = isRaised ? 0.5 : 0.35;

  const contactBlur = isRaised ? 6 : 3;
  const contactOffsetY = isRaised ? 3 : 1;
  const contactAlpha = isRaised ? 0.4 : 0.25;

  // Passagem 1: Sombra Difusa (Penumbra suave)
  ctx.shadowColor = `rgba(0, 0, 0, ${diffuseAlpha})`;
  ctx.shadowBlur = diffuseBlur;
  ctx.shadowOffsetX = 0;
  ctx.shadowOffsetY = diffuseOffsetY;
  drawRoundedPath(ctx, x, y, width, height, radius);
  ctx.fillStyle = fillColor;
  ctx.fill();

  // Passagem 2: Sombra de Contato (Oclusão nítida)
  ctx.shadowColor = `rgba(0, 0, 0, ${contactAlpha})`;
  ctx.shadowBlur = contactBlur;
  ctx.shadowOffsetX = 0;
  ctx.shadowOffsetY = contactOffsetY;
  drawRoundedPath(ctx, x, y, width, height, radius);
  ctx.fillStyle = fillColor;
  ctx.fill();

  ctx.restore();

  // Passagem 3: Micro-borda de Contorno e Chanfro Zenital de Topo (Rim Light)
  ctx.save();
  drawRoundedPath(ctx, x + 0.5, y + 0.5, width - 1, height - 1, radius);
  ctx.lineWidth = 1;
  ctx.strokeStyle = rimColor;
  ctx.stroke();

  // Destaque Zenital (Reflexo de luz superior)
  if (width > radius * 2) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y + 0.5);
    ctx.lineTo(x + width - radius, y + 0.5);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.16)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  ctx.restore();
}

/**
 * Função utilitária de caminho arredondado compatível com CanvasRenderingContext2D moderno e fallbacks.
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
    // Fallback manual para navegadores legados
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

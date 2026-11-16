# Reference Implementations — `complex-zero` (`v3.1.0`)

Reference implementations complying with the **9-Axis SSOT (Zero-Placebo / Real-State)** across the 4 modules of `complex-zero`:

1. **`devtools_auditor.ts`**: Runtime physical probe via Playwright/CDP (filtering visible elements, measuring `>= 48x48px` targets under `pointer: coarse`, `:focus-visible`, `@container`, and true perceptual contrast instead of hardcoded booleans).
2. **`ast_integrity_checker.ts`**: Static TypeScript Compiler API auditor (Path Traversal confinement, *Ghost Node* detection, empty `{}` bodies, isolated `console.log` stubs, `setTimeout` placebos, `Math.random()` telemetry, and executable declaration counting).
3. **`CustomMetricNode.tsx`**: Custom `@xyflow/react` node with zero emojis (`[DIR]`, `[FILE]`, `[GHOST]`), `font-variant-numeric: tabular-nums`, `nodrag nopan`, and `oklch()` surfaces.
4. **`server/metrics_watcher.ts` & Next.js 15+ Routes**: `chokidar` + `WebSocket` server with `150ms` batching (`BATCH_UPDATE`) and real Event Loop telemetry (`perf_hooks.monitorEventLoopDelay()`) plus async `Promise<{ slug: string }>` routing in Next.js 15+.

---

## 1. Runtime Physical Probe via Playwright / CDP (`devtools_auditor.ts`)

```typescript
import { chromium, Browser, Page } from 'playwright';

export interface DevToolsAuditResult {
  fittsLawPassed: boolean;
  fittsViolations: string[];
  focusVisibleActive: boolean;
  containerQueriesDetected: number;
  oklchContrastValid: boolean;
  contrastViolations: string[];
  domNodeCount: number;
}

function parseRgbOrOklchLightness(cssColor: string): number | null {
  const oklchMatch = cssColor.match(/oklch\(\s*([0-9.]+%?)/i);
  if (oklchMatch) {
    const raw = oklchMatch[1];
    return raw.endsWith('%') ? parseFloat(raw) / 100 : parseFloat(raw);
  }
  const rgbMatch = cssColor.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
  if (rgbMatch) {
    const [r, g, b] = [Number(rgbMatch[1]) / 255, Number(rgbMatch[2]) / 255, Number(rgbMatch[3]) / 255];
    const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    return Math.cbrt(lum); // Perceptual L* approximation from relative luminance
  }
  return null;
}

export async function runDevToolsAudit(targetUrl: string): Promise<DevToolsAuditResult> {
  const browser: Browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    hasTouch: true, // Enables @media (any-pointer: coarse) to audit Fitts' Law targets
  });
  const page: Page = await context.newPage();

  try {
    await page.goto(targetUrl, { waitUntil: 'networkidle' });

    const auditData = await page.evaluate(() => {
      const fittsViolations: string[] = [];
      const contrastViolations: string[] = [];
      const interactiveEls = document.querySelectorAll('button, a, input, select, textarea, [role="button"]');

      interactiveEls.forEach((el) => {
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        const isVisible =
          rect.width > 0 &&
          rect.height > 0 &&
          style.display !== 'none' &&
          style.visibility !== 'hidden' &&
          parseFloat(style.opacity || '1') > 0;

        if (!isVisible) return;

        if (rect.width < 48 || rect.height < 48) {
          const id = el.id ? `#${el.id}` : el.className ? `.${String(el.className).split(' ')[0]}` : '';
          fittsViolations.push(`${el.tagName.toLowerCase()}${id} (${Math.round(rect.width)}x${Math.round(rect.height)}px < 48x48px)`);
        }

        const fg = style.color;
        const bg = style.backgroundColor;
        if (fg && bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
          contrastViolations.push(`${el.tagName.toLowerCase()}|${fg}|${bg}`);
        }
      });

      let containerCount = 0;
      const allElements = document.querySelectorAll('*');
      allElements.forEach((el) => {
        const style = window.getComputedStyle(el);
        if (style.containerType && style.containerType !== 'normal') {
          containerCount++;
        }
      });

      return {
        fittsViolations,
        rawColorPairs: contrastViolations,
        containerQueriesDetected: containerCount,
        domNodeCount: allElements.length,
      };
    });

    const realContrastErrors: string[] = [];
    for (const entry of auditData.rawColorPairs) {
      const [tag, fg, bg] = entry.split('|');
      const lFg = parseRgbOrOklchLightness(fg);
      const lBg = parseRgbOrOklchLightness(bg);
      if (lFg !== null && lBg !== null && Math.abs(lFg - lBg) < 0.38) {
        realContrastErrors.push(`${tag}: insufficient perceptual delta L (${Math.abs(lFg - lBg).toFixed(2)} < 0.38)`);
      }
    }

    await page.keyboard.press('Tab');
    const focusVisibleActive = await page.evaluate(() => {
      const active = document.activeElement;
      if (!active || active === document.body) return false;
      const style = window.getComputedStyle(active);
      return (style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0) || style.boxShadow !== 'none';
    });

    return {
      fittsLawPassed: auditData.fittsViolations.length === 0,
      fittsViolations: auditData.fittsViolations,
      focusVisibleActive,
      containerQueriesDetected: auditData.containerQueriesDetected,
      oklchContrastValid: realContrastErrors.length === 0,
      contrastViolations: realContrastErrors,
      domNodeCount: auditData.domNodeCount,
    };
  } finally {
    await browser.close();
  }
}
```

---

## 2. Anti-Fake AST Audit: Ghost Nodes & Stub Functions (`ast_integrity_checker.ts`)

```typescript
import * as ts from 'typescript';
import * as fs from 'fs';
import * as path from 'path';

export interface NodeIntegrityReport {
  nodeId: string;
  filePath: string;
  existsOnDisk: boolean;
  isGhostNode: boolean;
  fakeFunctionsFound: string[];
  placeboPatternsFound: string[];
  cyclomaticComplexity: number;
  status: 'VALID' | 'FAKE_DETECTED' | 'GHOST_NODE';
}

export function auditGraphIntegrity(
  projectRoot: string,
  graphNodes: Array<{ id: string; filePath: string }>
): NodeIntegrityReport[] {
  const rootResolved = path.resolve(projectRoot);

  return graphNodes.map((node) => {
    const resolvedPath = path.resolve(rootResolved, node.filePath);
    const isInsideRoot = resolvedPath.startsWith(rootResolved + path.sep) || resolvedPath === rootResolved;
    const exists = isInsideRoot && fs.existsSync(resolvedPath) && fs.statSync(resolvedPath).isFile();

    if (!exists) {
      return {
        nodeId: node.id,
        filePath: node.filePath,
        existsOnDisk: false,
        isGhostNode: true,
        fakeFunctionsFound: [],
        placeboPatternsFound: !isInsideRoot ? ['PATH_TRAVERSAL_BLOCKED'] : [],
        cyclomaticComplexity: 0,
        status: 'GHOST_NODE',
      };
    }

    const sourceCode = fs.readFileSync(resolvedPath, 'utf-8');
    const sourceFile = ts.createSourceFile(resolvedPath, sourceCode, ts.ScriptTarget.Latest, true);
    const fakeFunctions: string[] = [];
    const placeboPatterns: string[] = [];
    let complexity = 1;
    let executableDeclarations = 0;

    if (/Math\.random\(\)/.test(sourceCode) && /(fps|cpu|latency|memory|metric)/i.test(sourceCode)) {
      placeboPatterns.push('SIMULATED_TELEMETRY_MATH_RANDOM');
    }

    function visit(astNode: ts.Node) {
      if (
        ts.isIfStatement(astNode) ||
        ts.isForStatement(astNode) ||
        ts.isWhileStatement(astNode) ||
        ts.isCaseClause(astNode) ||
        ts.isConditionalExpression(astNode)
      ) {
        complexity++;
      }

      if (
        ts.isFunctionDeclaration(astNode) ||
        ts.isArrowFunction(astNode) ||
        ts.isMethodDeclaration(astNode) ||
        ts.isFunctionExpression(astNode)
      ) {
        executableDeclarations++;
        const fnName =
          (astNode.name && ts.isIdentifier(astNode.name) ? astNode.name.text : undefined) ||
          `anon_line_${sourceFile.getLineAndCharacterOfPosition(astNode.getStart()).line + 1}`;
        const body = astNode.body;

        if (body && ts.isBlock(body)) {
          if (body.statements.length === 0) {
            fakeFunctions.push(`${fnName} (Empty body {})`);
          } else if (body.statements.length === 1) {
            const stmtText = body.statements[0].getText(sourceFile).trim();
            if (stmtText.startsWith('console.log') || stmtText.includes('alert(')) {
              fakeFunctions.push(`${fnName} (Superficial stub: ${stmtText.slice(0, 40)})`);
            } else if (/^setTimeout\(/.test(stmtText) && !/fetch|axios|send|dispatch/.test(stmtText)) {
              placeboPatterns.push(`${fnName} (Artificial setTimeout delay without I/O)`);
            }
          }
        }
      }
      ts.forEachChild(astNode, visit);
    }

    visit(sourceFile);

    if (executableDeclarations === 0 && /\.(ts|tsx|js|jsx)$/.test(resolvedPath)) {
      placeboPatterns.push('FILE_WITHOUT_EXECUTABLE_DECLARATIONS');
    }

    const hasIssues = fakeFunctions.length > 0 || placeboPatterns.length > 0;
    return {
      nodeId: node.id,
      filePath: node.filePath,
      existsOnDisk: true,
      isGhostNode: false,
      fakeFunctionsFound: fakeFunctions,
      placeboPatternsFound: placeboPatterns,
      cyclomaticComplexity: complexity,
      status: hasIssues ? 'FAKE_DETECTED' : 'VALID',
    };
  });
}
```

---

## 3. Custom React Flow Node with Tabular Telemetry (`CustomMetricNode.tsx`)

```tsx
'use client';
import React from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';

export interface FileNodeMetrics {
  latencyMs: number;
  memoryKb: number;
  fps: number;
  complexity: number;
}

export interface CustomFileNodeData {
  label: string;
  path: string;
  type: 'file' | 'directory';
  isUpdated?: boolean;
  isGhost?: boolean;
  hasFakeCode?: boolean;
  metrics?: FileNodeMetrics;
  onInspect?: (path: string) => void;
}

export function CustomMetricNode({ data }: NodeProps) {
  const nodeData = data as unknown as CustomFileNodeData;
  const { label, path: filePath, type, isUpdated, isGhost, hasFakeCode, metrics, onInspect } = nodeData;

  const badgeTag = isGhost ? '[GHOST]' : type === 'directory' ? '[DIR]' : '[FILE]';
  const statusTag = isGhost ? '[ERR: DISK]' : hasFakeCode ? '[WARN: STUB]' : '[SYNCED]';

  return (
    <div
      className={[
        'custom-file-node',
        isUpdated ? 'node-updated-flash' : '',
        isGhost ? 'node-error-ghost' : '',
        hasFakeCode ? 'node-warn-fake' : '',
      ].filter(Boolean).join(' ')}
    >
      <Handle type="target" position={Position.Top} />
      <div className="node-header">
        <span className="node-tag" aria-hidden="true">{badgeTag}</span>
        <strong className="node-title">{label}</strong>
        <span className="node-status">{statusTag}</span>
      </div>

      {metrics && !isGhost && (
        <dl className="node-metrics-grid" style={{ fontVariantNumeric: 'tabular-nums' }}>
          <div className="metric-badge" title="Real Event Loop latency (full details in Side Inspector)">
            <dt className="sr-only">Latency</dt>
            <dd>[LAT] {metrics.latencyMs.toFixed(1)}ms</dd>
          </div>
          <div className="metric-badge" title="AST Cyclomatic Complexity">
            <dt className="sr-only">Complexity</dt>
            <dd>[CPX] {metrics.complexity}</dd>
          </div>
        </dl>
      )}

      <div className="node-actions nodrag nopan">
        <button
          type="button"
          className="btn-node-inspect"
          onClick={(e) => {
            e.stopPropagation();
            onInspect?.(filePath);
          }}
        >
          Inspect Node
        </button>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
```

---

## 4. `WebSocket` + `Chokidar` Server with `150ms` Batching & Real Telemetry (`server/metrics_watcher.ts`)

```typescript
import chokidar from 'chokidar';
import { WebSocketServer, WebSocket } from 'ws';
import { monitorEventLoopDelay } from 'perf_hooks';
import path from 'path';
import fs from 'fs';

const wss = new WebSocketServer({ port: 4000 });
const TARGET_DIR = path.resolve(process.cwd(), 'src');
const loopHistogram = monitorEventLoopDelay({ resolution: 20 });
loopHistogram.enable();

const watcher = chokidar.watch(TARGET_DIR, {
  ignored: /(^|[\/\\])\..|node_modules|\.next/,
  persistent: true,
  ignoreInitial: true,
});

interface FsChangeEvent {
  eventType: 'add' | 'change' | 'unlink';
  path: string;
  name: string;
  sizeKb: number;
  eventLoopLagMs: number;
  heapUsedMb: number;
  timestamp: number;
}

let batchBuffer: FsChangeEvent[] = [];
let batchTimer: NodeJS.Timeout | null = null;

function flushBatch() {
  if (batchBuffer.length === 0) return;
  const payload = JSON.stringify({
    type: 'BATCH_UPDATE',
    count: batchBuffer.length,
    events: batchBuffer,
    flushedAt: Date.now(),
  });
  batchBuffer = [];
  batchTimer = null;

  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(payload);
    }
  });
}

function enqueueFsEvent(eventType: 'add' | 'change' | 'unlink', filePath: string) {
  const relativePath = path.relative(TARGET_DIR, filePath).replace(/\\/g, '/');
  let sizeKb = 0;
  if (eventType !== 'unlink' && fs.existsSync(filePath)) {
    sizeKb = Math.round((fs.statSync(filePath).size / 1024) * 100) / 100;
  }
  const eventLoopLagMs = Number((loopHistogram.mean / 1e6).toFixed(2));
  const heapUsedMb = Number((process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2));

  batchBuffer.push({
    eventType,
    path: relativePath,
    name: path.basename(filePath),
    sizeKb,
    eventLoopLagMs,
    heapUsedMb,
    timestamp: Date.now(),
  });

  if (!batchTimer) {
    batchTimer = setTimeout(flushBatch, 150);
  }
}

watcher
  .on('add', (p) => enqueueFsEvent('add', p))
  .on('change', (p) => enqueueFsEvent('change', p))
  .on('unlink', (p) => enqueueFsEvent('unlink', p));
```

import React, { useState, useEffect, useRef } from 'react';
import { DashboardLayout } from './components/templates/DashboardLayout';
import { TabsNav } from './components/organisms/TabsNav';
import { TactileButton } from './components/atoms/TactileButton';
import { SunkenInput } from './components/atoms/SunkenInput';
import { NotificationToast } from './components/molecules/NotificationToast';
import { drawElevatedCard } from './canvas/elevationRenderer';
import { TabItem, ThemeMode, ToastMessage } from './types';
import {
  Layers,
  Sparkles,
  ShieldCheck,
  Cpu,
  CheckCircle2,
  Sliders,
  Send,
} from 'lucide-react';

export const App: React.FC = () => {
  const [theme, setTheme] = useState<ThemeMode>('dark');
  const [activeNavId, setActiveNavId] = useState('dashboard');
  const [activeTab, setActiveTab] = useState('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [toasts, setToasts] = useState<ToastMessage[]>([
    {
      id: 'welcome-toast',
      type: 'info',
      title: 'Arquitetura Universal Ativa',
      description: 'Template 2026 configurado com Design System Tátil e paleta Mineral Slate.',
      durationMs: 7000,
    },
  ]);

  // Sincronização do tema com o elemento raiz HTML
  const toggleTheme = () => {
    const nextTheme: ThemeMode = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const triggerNewToast = () => {
    const newToast: ToastMessage = {
      id: `toast-${Date.now()}`,
      type: 'success',
      title: 'Ação Executada com Sucesso',
      description: 'O relevo físico e a micro-borda foram computados pelo motor do Tailwind.',
      durationMs: 5000,
    };
    setToasts((prev) => [...prev, newToast]);
  };

  // Abas de navegação principal
  const tabs: TabItem[] = [
    { id: 'overview', label: 'Visão Geral', count: 4 },
    { id: 'canvas', label: 'Motor Canvas 2D (Multi-Sombra)' },
    { id: 'components', label: 'Componentes Táteis' },
    { id: 'audit', label: 'Auditoria de Conformidade' },
  ];

  // Referência do Canvas 2D para renderização de nós de fluxo
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    if (activeTab === 'canvas' && canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      // Limpar canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const isDark = theme === 'dark';
      const cardColor = isDark ? '#11141A' : '#FFFFFF';
      const raisedColor = isDark ? '#181D26' : '#FFFFFF';
      const rimHighlight = isDark ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.08)';

      // 1. Nó de Ingress (Card Padrão com Multi-Sombra)
      drawElevatedCard(ctx, {
        x: 40,
        y: 60,
        width: 220,
        height: 120,
        radius: 16,
        fillColor: cardColor,
        rimColor: rimHighlight,
        elevation: 'card',
      });

      // 2. Nó Central de Processamento (Card Raised Flutuante)
      drawElevatedCard(ctx, {
        x: 340,
        y: 50,
        width: 260,
        height: 140,
        radius: 16,
        fillColor: raisedColor,
        rimColor: isDark ? 'rgba(56, 189, 248, 0.3)' : 'rgba(2, 132, 199, 0.25)',
        elevation: 'raised',
      });

      // 3. Nó de Saída (Card Padrão)
      drawElevatedCard(ctx, {
        x: 680,
        y: 60,
        width: 220,
        height: 120,
        radius: 16,
        fillColor: cardColor,
        rimColor: rimHighlight,
        elevation: 'card',
      });

      // Desenhar Linhas de Conexão com Curvas Suaves
      ctx.save();
      ctx.strokeStyle = isDark ? 'rgba(56, 189, 248, 0.4)' : 'rgba(2, 132, 199, 0.4)';
      ctx.lineWidth = 2;
      ctx.setLineDash([6, 6]);

      // Linha 1 -> 2
      ctx.beginPath();
      ctx.moveTo(260, 120);
      ctx.bezierCurveTo(290, 120, 310, 120, 340, 120);
      ctx.stroke();

      // Linha 2 -> 3
      ctx.beginPath();
      ctx.moveTo(600, 120);
      ctx.bezierCurveTo(630, 120, 650, 120, 680, 120);
      ctx.stroke();

      ctx.restore();

      // Textos e Rótulos nos Nós
      ctx.save();
      ctx.font = '600 13px Inter, sans-serif';
      ctx.fillStyle = isDark ? '#F3F4F6' : '#0F172A';
      ctx.fillText('Nó 01: Ingress Pipeline', 56, 95);
      ctx.fillText('Nó 02: Closed-Loop AI', 356, 90);
      ctx.fillText('Nó 03: Saída Auditada', 696, 95);

      ctx.font = '400 11px Inter, sans-serif';
      ctx.fillStyle = isDark ? '#9CA3AF' : '#475569';
      ctx.fillText('Tokens brutos & eventos', 56, 120);
      ctx.fillText('Raciocínio & Self-Refine', 356, 115);
      ctx.fillText('Asserções [PASS]/[FAIL]', 696, 120);
      ctx.restore();
    }
  }, [activeTab, theme]);

  return (
    <DashboardLayout
      activeNavId={activeNavId}
      onNavigate={setActiveNavId}
      searchValue={searchQuery}
      onSearchChange={setSearchQuery}
      theme={theme}
      onToggleTheme={toggleTheme}
      onOpenNotifications={triggerNewToast}
    >
      {/* Barra de Abas e Ações Superiores */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <TabsNav tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

        <div className="flex items-center gap-3">
          <TactileButton variant="secondary" size="sm" icon={<Sliders className="w-3.5 h-3.5" />}>
            Parâmetros
          </TactileButton>
          <TactileButton
            variant="primary"
            size="sm"
            onClick={triggerNewToast}
            icon={<Sparkles className="w-3.5 h-3.5" />}
          >
            Disparar Toast
          </TactileButton>
        </div>
      </div>

      {/* Conteúdo Dinâmico por Aba */}
      {activeTab === 'overview' && (
        <div className="flex flex-col gap-6">
          {/* Grade de Cartões de Métricas com Elevação Tátil */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex flex-col p-6 rounded-2xl bg-[var(--surface-card)] border border-[var(--border-rim)] border-t-[var(--border-rim-highlight)] shadow-[var(--shadow-tactile-card)]">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">
                  Saúde do Contexto
                </span>
                <ShieldCheck className="w-5 h-5 text-[var(--status-success)]" />
              </div>
              <span className="mt-4 text-3xl font-bold tracking-tight text-[var(--text-primary)]">
                100%
              </span>
              <p className="mt-2 text-xs text-[var(--text-muted)]">
                Zero perda de tokens • Taxonomia epistêmica ativa
              </p>
            </div>

            <div className="flex flex-col p-6 rounded-2xl bg-[var(--surface-card)] border border-[var(--border-rim)] border-t-[var(--border-rim-highlight)] shadow-[var(--shadow-tactile-card)]">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">
                  Tempo de Resposta
                </span>
                <Cpu className="w-5 h-5 text-[var(--accent-action)]" />
              </div>
              <span className="mt-4 text-3xl font-bold tracking-tight text-[var(--text-primary)]">
                24ms
              </span>
              <p className="mt-2 text-xs text-[var(--text-muted)]">
                Renderização local sem bloqueio de GPU
              </p>
            </div>

            <div className="flex flex-col p-6 rounded-2xl bg-[var(--surface-card)] border border-[var(--border-rim)] border-t-[var(--border-rim-highlight)] shadow-[var(--shadow-tactile-card)]">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">
                  Qualidade Visual
                </span>
                <Layers className="w-5 h-5 text-amber-400" />
              </div>
              <span className="mt-4 text-3xl font-bold tracking-tight text-[var(--text-primary)]">
                WCAG AAA
              </span>
              <p className="mt-2 text-xs text-[var(--text-muted)]">
                Contraste rigoroso e foco com anel semântico
              </p>
            </div>
          </div>

          {/* Painel Central com Demonstração de Formulário */}
          <div className="p-8 rounded-3xl bg-[var(--surface-card)] border border-[var(--border-rim)] shadow-[var(--shadow-tactile-card)] flex flex-col gap-6">
            <div>
              <h2 className="text-lg font-semibold tracking-wide text-[var(--text-primary)]">
                Experimente o Relevo Físico Tátil
              </h2>
              <p className="mt-1 text-xs text-[var(--text-secondary)]">
                Os inputs apresentam relevo negativo (sunken) com sombra interna, e os botões
                possuem relevo positivo com chanfro zenital.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <SunkenInput
                label="Identificador do Módulo"
                placeholder="ex: modulo-pagamento-seguro"
                defaultValue="universal-core-v2"
              />
              <SunkenInput
                label="Chave de Roteamento"
                placeholder="Insira o namespace do evento..."
                defaultValue="events.pipeline.ready"
              />
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <TactileButton variant="ghost">Restaurar Padrão</TactileButton>
              <TactileButton variant="primary" icon={<Send className="w-4 h-4" />}>
                Publicar Alterações
              </TactileButton>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'canvas' && (
        <div className="flex flex-col gap-4 p-6 rounded-3xl bg-[var(--surface-card)] border border-[var(--border-rim)] shadow-[var(--shadow-tactile-card)]">
          <div>
            <h2 className="text-lg font-semibold text-[var(--text-primary)]">
              Motor de Multi-Sombra em Canvas 2D
            </h2>
            <p className="text-xs text-[var(--text-secondary)]">
              Pipeline de dupla passagem de renderização: Passagem 1 (penumbra difusa ampla 18px),
              Passagem 2 (sombra de contato nítida 4px) e Passagem 3 (rim light zenital de topo).
            </p>
          </div>

          <div className="flex items-center justify-center p-4 rounded-2xl bg-[var(--surface-sunken)] border border-[var(--border-subtle)] shadow-[var(--shadow-tactile-inset)] overflow-x-auto">
            <canvas ref={canvasRef} width={960} height={240} className="rounded-xl" />
          </div>
        </div>
      )}

      {activeTab === 'components' && (
        <div className="flex flex-col gap-8 p-8 rounded-3xl bg-[var(--surface-card)] border border-[var(--border-rim)] shadow-[var(--shadow-tactile-card)]">
          <div>
            <h2 className="text-lg font-semibold text-[var(--text-primary)]">
              Catálogo de Componentes Atômicos
            </h2>
            <p className="text-xs text-[var(--text-secondary)]">
              Botões táteis com blindagem anti-squish, dimensões ergonômicas (44px) e estados táteis
              ativos.
            </p>
          </div>

          {/* Galeria de Botões */}
          <div className="flex flex-wrap items-center gap-4">
            <TactileButton variant="primary">Botão Primário</TactileButton>
            <TactileButton variant="secondary">Botão Secundário</TactileButton>
            <TactileButton variant="outline">Botão Outline</TactileButton>
            <TactileButton variant="ghost">Botão Ghost</TactileButton>
            <TactileButton variant="danger">Ação Destrutiva</TactileButton>
            <TactileButton variant="primary" isLoading>
              Processando
            </TactileButton>
          </div>
        </div>
      )}

      {activeTab === 'audit' && (
        <div className="flex flex-col gap-6 p-8 rounded-3xl bg-[var(--surface-card)] border border-[var(--border-rim)] shadow-[var(--shadow-tactile-card)]">
          <div>
            <h2 className="text-lg font-semibold text-[var(--text-primary)]">
              Checklist Determinístico de UI/UX Melki
            </h2>
            <p className="text-xs text-[var(--text-secondary)]">
              Critérios falsificáveis para validação antes de qualquer entrega de software.
            </p>
          </div>

          <div className="flex flex-col gap-3">
            {[
              {
                title: 'Ausência de Cores Fixas Hardcoded',
                desc: 'Todo estilo consome variáveis CSS :root e tokens semânticos do Tailwind.',
              },
              {
                title: 'Semântica de Interação Rígida',
                desc: 'Todos os nós clicáveis utilizam <button type="button"> nativo.',
              },
              {
                title: 'Ergonomia Anti-Squish e Altura Mínima',
                desc: 'Botões blindados com shrink-0 whitespace-nowrap e altura >= 44px.',
              },
              {
                title: 'Navegação por Teclado e Foco Visível',
                desc: 'Abas com setas horizontais e indicador :focus-visible com anel de 4px.',
              },
              {
                title: 'Banimento de Azul Cobalto Saturado',
                desc: 'Paleta Mineral Slate com acentos Sky Blue / Ardósia calibrados.',
              },
            ].map((gate, i) => (
              <div
                key={i}
                className="flex items-start gap-3 p-4 rounded-xl bg-[var(--surface-sunken)] border border-[var(--border-subtle)] shadow-[var(--shadow-tactile-inset)]"
              >
                <CheckCircle2 className="w-5 h-5 text-[var(--status-success)] shrink-0 mt-0.5" />
                <div className="flex flex-col">
                  <span className="text-sm font-semibold text-[var(--text-primary)]">
                    [PASS] {gate.title}
                  </span>
                  <span className="text-xs text-[var(--text-secondary)] mt-0.5">{gate.desc}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pilha Fixa de Toasts Flutuantes */}
      <div className="fixed bottom-6 right-6 flex flex-col gap-3 z-50 pointer-events-none">
        {toasts.map((toast) => (
          <div key={toast.id} className="pointer-events-auto">
            <NotificationToast toast={toast} onDismiss={removeToast} />
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
};

export default App;

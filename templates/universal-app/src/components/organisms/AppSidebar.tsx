import React from 'react';
import {
  Compass,
  FolderGit2,
  HardDrive,
  Layers,
  Settings,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import { NavItem } from '../../types';

export interface AppSidebarProps {
  activeId: string;
  onNavigate: (id: string) => void;
  brandName?: string;
  systemVersion?: string;
}

export const AppSidebar: React.FC<AppSidebarProps> = ({
  activeId,
  onNavigate,
  brandName = 'Franklin Quebra-Galho',
  systemVersion = 'v2.0.0',
}) => {
  const navItems: NavItem[] = [
    { id: 'dashboard', label: 'Painel Geral', iconName: 'Compass' },
    { id: 'canvas-nodes', label: 'Motor Canvas 2D', iconName: 'Layers', badge: 'Novo' },
    { id: 'drive', label: 'Google Drive Sync', iconName: 'HardDrive' },
    { id: 'projects', label: 'Projetos Ativos', iconName: 'FolderGit2', badge: 12 },
    { id: 'security', label: 'Auditoria Zero-Trust', iconName: 'ShieldCheck' },
    { id: 'settings', label: 'Configurações', iconName: 'Settings' },
  ];

  const getIcon = (name: string) => {
    switch (name) {
      case 'Compass':
        return <Compass className="w-4 h-4 shrink-0" />;
      case 'Layers':
        return <Layers className="w-4 h-4 shrink-0 text-[var(--accent-action)]" />;
      case 'HardDrive':
        return <HardDrive className="w-4 h-4 shrink-0" />;
      case 'FolderGit2':
        return <FolderGit2 className="w-4 h-4 shrink-0" />;
      case 'ShieldCheck':
        return <ShieldCheck className="w-4 h-4 shrink-0 text-[var(--status-success)]" />;
      case 'Settings':
        return <Settings className="w-4 h-4 shrink-0" />;
      default:
        return <Sparkles className="w-4 h-4 shrink-0" />;
    }
  };

  return (
    <aside
      aria-label="Menu Lateral de Navegação"
      className="
        flex flex-col justify-between
        w-68 h-screen
        bg-[var(--canvas-bg)]
        border-r border-[var(--border-rim)]
        select-none
      "
    >
      {/* Cabeçalho da Sidebar: Identidade da Marca com Respiro */}
      <div className="flex flex-col">
        <div className="flex items-center gap-3 px-6 h-18 border-b border-[var(--border-subtle)]">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-[var(--surface-card)] border border-[var(--border-rim-highlight)] shadow-[var(--shadow-tactile-card)]">
            <Sparkles className="w-5 h-5 text-[var(--accent-action)]" />
          </div>
          <div className="flex flex-col">
            <h1 className="text-sm font-semibold tracking-wide text-[var(--text-primary)]">
              {brandName}
            </h1>
            <span className="text-[11px] font-mono text-[var(--text-muted)]">
              {systemVersion} • Universal
            </span>
          </div>
        </div>

        {/* Lista de Navegação Principal: Espaçamento Nobre Anti-Compactação */}
        <nav className="flex flex-col gap-1.5 p-4 mt-2">
          {navItems.map((item) => {
            const isActive = activeId === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onNavigate(item.id)}
                className={`
                  flex items-center justify-between
                  h-11 px-3.5 gap-3
                  rounded-xl
                  text-sm font-medium tracking-wide
                  transition-all duration-150 ease-out
                  focus-visible:outline-none
                  focus-visible:ring-2
                  focus-visible:ring-[var(--accent-action)]
                  ${
                    isActive
                      ? 'bg-[var(--surface-card)] text-[var(--text-primary)] shadow-[var(--shadow-tactile-card)] border-t border-[var(--border-rim-highlight)] font-semibold'
                      : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[rgba(255,255,255,0.03)]'
                  }
                `}
              >
                <div className="flex items-center gap-3 min-w-0">
                  {getIcon(item.iconName)}
                  <span className="truncate">{item.label}</span>
                </div>

                {item.badge !== undefined && (
                  <span
                    className={`
                      px-2 py-0.5 text-[10px] rounded-full font-mono font-semibold shrink-0
                      ${
                        isActive
                          ? 'bg-[var(--accent-action)] text-slate-950 font-bold'
                          : 'bg-[var(--surface-sunken)] text-[var(--text-muted)] border border-[var(--border-subtle)]'
                      }
                    `}
                  >
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Rodapé da Sidebar */}
      <div className="p-4 border-t border-[var(--border-subtle)]">
        <div className="flex items-center gap-3 p-3 rounded-xl bg-[var(--surface-sunken)] border border-[var(--border-subtle)] shadow-[var(--shadow-tactile-inset)]">
          <div className="w-8 h-8 rounded-lg bg-[var(--surface-card)] border border-[var(--border-rim)] flex items-center justify-center text-xs font-bold text-[var(--accent-action)]">
            M
          </div>
          <div className="flex flex-col min-w-0">
            <span className="text-xs font-semibold text-[var(--text-primary)] truncate">
              Melki Dev
            </span>
            <span className="text-[10px] text-[var(--text-muted)] truncate">
              Arquiteto de Soluções
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
};

import React from 'react';
import { AppSidebar } from '../organisms/AppSidebar';
import { SearchBar } from '../molecules/SearchBar';
import { TactileButton } from '../atoms/TactileButton';
import { Bell, Moon, Sun } from 'lucide-react';
import { ThemeMode } from '../../types';

export interface DashboardLayoutProps {
  children: React.ReactNode;
  activeNavId: string;
  onNavigate: (id: string) => void;
  searchValue: string;
  onSearchChange: (value: string) => void;
  theme: ThemeMode;
  onToggleTheme: () => void;
  onOpenNotifications?: () => void;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  activeNavId,
  onNavigate,
  searchValue,
  onSearchChange,
  theme,
  onToggleTheme,
  onOpenNotifications,
}) => {
  return (
    <div className="flex w-full min-h-screen bg-[var(--canvas-bg)] text-[var(--text-primary)]">
      {/* Sidebar de Navegação */}
      <AppSidebar activeId={activeNavId} onNavigate={onNavigate} />

      {/* Conteúdo Principal com Top Header Fixo */}
      <div className="flex flex-col flex-1 min-w-0 h-screen overflow-hidden">
        {/* Top Header com Respiro e Controles Táteis */}
        <header className="flex items-center justify-between px-8 h-18 bg-[var(--canvas-bg)]/80 backdrop-blur-md border-b border-[var(--border-subtle)] shrink-0 z-10">
          <div className="flex-1 max-w-md">
            <SearchBar value={searchValue} onChange={onSearchChange} />
          </div>

          <div className="flex items-center gap-3">
            {/* Alternador de Tema */}
            <TactileButton
              variant="outline"
              size="sm"
              onClick={onToggleTheme}
              aria-label="Alternar modo escuro e claro"
            >
              {theme === 'dark' ? (
                <Sun className="w-4 h-4 text-amber-400" />
              ) : (
                <Moon className="w-4 h-4 text-slate-700" />
              )}
            </TactileButton>

            {/* Sino de Notificações */}
            <TactileButton
              variant="secondary"
              size="sm"
              onClick={onOpenNotifications}
              aria-label="Notificações do sistema"
            >
              <Bell className="w-4 h-4 text-[var(--accent-action)]" />
            </TactileButton>

            {/* Botão de Ação Primária */}
            <TactileButton variant="primary" size="sm">
              Novo Projeto
            </TactileButton>
          </div>
        </header>

        {/* Área de Visualização com Scroll Suave */}
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto flex flex-col gap-8">{children}</div>
        </main>
      </div>
    </div>
  );
};

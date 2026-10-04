import React, { useRef } from 'react';
import { TabItem } from '../../types';

export interface TabsNavProps {
  tabs: TabItem[];
  activeTab: string;
  onTabChange: (id: string) => void;
  ariaLabel?: string;
}

export const TabsNav: React.FC<TabsNavProps> = ({
  tabs,
  activeTab,
  onTabChange,
  ariaLabel = 'Abas de Navegação Principal',
}) => {
  const tabsRef = useRef<(HTMLButtonElement | null)[]>([]);

  // Navegação horizontal ergonômica por teclado (W3C WAI-ARIA Tabs Design Pattern)
  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let nextIndex: number | null = null;

    if (e.key === 'ArrowRight') {
      nextIndex = (index + 1) % tabs.length;
    } else if (e.key === 'ArrowLeft') {
      nextIndex = (index - 1 + tabs.length) % tabs.length;
    } else if (e.key === 'Home') {
      nextIndex = 0;
    } else if (e.key === 'End') {
      nextIndex = tabs.length - 1;
    }

    if (nextIndex !== null) {
      e.preventDefault();
      const targetTab = tabs[nextIndex];
      if (!targetTab.disabled) {
        tabsRef.current[nextIndex]?.focus();
        onTabChange(targetTab.id);
      }
    }
  };

  return (
    <nav
      role="tablist"
      aria-label={ariaLabel}
      className="
        inline-flex items-center p-1.5 gap-1.5
        bg-[var(--surface-sunken)]
        rounded-2xl
        border border-[var(--border-subtle)]
        shadow-[var(--shadow-tactile-inset)]
      "
    >
      {tabs.map((tab, idx) => {
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            ref={(el) => (tabsRef.current[idx] = el)}
            role="tab"
            type="button"
            id={`tab-${tab.id}`}
            aria-selected={isActive}
            aria-controls={`panel-${tab.id}`}
            tabIndex={isActive ? 0 : -1}
            disabled={tab.disabled}
            onClick={() => onTabChange(tab.id)}
            onKeyDown={(e) => handleKeyDown(e, idx)}
            className={`
              relative inline-flex items-center justify-center
              h-9 px-4 gap-2
              shrink-0 whitespace-nowrap select-none
              text-xs font-semibold tracking-wider uppercase
              rounded-xl
              transition-all duration-150 ease-out
              focus-visible:outline-none
              focus-visible:ring-2
              focus-visible:ring-[var(--accent-action)]
              focus-visible:ring-offset-2
              focus-visible:ring-offset-[var(--surface-sunken)]
              disabled:opacity-40 disabled:cursor-not-allowed
              ${
                isActive
                  ? 'bg-[var(--surface-card)] text-[var(--text-primary)] shadow-[var(--shadow-tactile-card)] border-t border-[var(--border-rim-highlight)]'
                  : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[rgba(255,255,255,0.03)]'
              }
            `}
          >
            <span>{tab.label}</span>
            {tab.count !== undefined && (
              <span
                className={`
                  px-2 py-0.5 text-[10px] rounded-full font-mono font-bold
                  transition-colors duration-150
                  ${
                    isActive
                      ? 'bg-[var(--accent-action)] text-slate-950'
                      : 'bg-[rgba(255,255,255,0.08)] text-[var(--text-secondary)]'
                  }
                `}
              >
                {tab.count}
              </span>
            )}
          </button>
        );
      })}
    </nav>
  );
};

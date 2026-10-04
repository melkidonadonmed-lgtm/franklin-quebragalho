export type ThemeMode = 'dark' | 'light';

export interface TabItem {
  id: string;
  label: string;
  count?: number;
  disabled?: boolean;
}

export type ToastVariant = 'info' | 'success' | 'warning' | 'danger';

export interface ToastMessage {
  id: string;
  type: ToastVariant;
  title: string;
  description?: string;
  durationMs?: number;
}

export interface NavItem {
  id: string;
  label: string;
  iconName: string;
  badge?: string | number;
  isActive?: boolean;
}

export interface ElevationCanvasOptions {
  x: number;
  y: number;
  width: number;
  height: number;
  radius: number;
  fillColor: string;
  rimColor?: string;
  elevation?: 'flat' | 'card' | 'raised';
}

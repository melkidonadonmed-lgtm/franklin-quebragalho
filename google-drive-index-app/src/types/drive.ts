export type MimeCategory = 'all' | 'document' | 'spreadsheet' | 'pdf' | 'folder' | 'image' | 'code';

export interface DriveFile {
  id: string;
  name: string;
  mimeType: string;
  sizeBytes?: number;
  modifiedTime: string;
  owners: string[];
  webViewLink?: string;
  folderCategory?: string;
  isStarred?: boolean;
}

export interface DriveStats {
  totalFiles: number;
  totalSizeBytes: number;
  categoryCounts: Record<MimeCategory, number>;
}

export type SortField = 'name' | 'sizeBytes' | 'modifiedTime';
export type SortOrder = 'asc' | 'desc';

export interface DriveQuery {
  searchTerm: string;
  category: MimeCategory;
  sortField: SortField;
  sortOrder: SortOrder;
}

export interface UserProfile {
  name: string;
  email?: string;
  avatarUrl?: string;
}

export type DataSourceMode = 'demo' | 'google-drive';

export interface ToastInfo {
  message: string;
  type: 'success' | 'error' | 'info';
}

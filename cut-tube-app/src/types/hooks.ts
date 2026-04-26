import type { Modal } from "@/types/app";

export interface UseForm<T> {
  formState: T;
  onInputChange: React.ChangeEventHandler<HTMLInputElement>;
  onResetForm: () => void;
}

export interface UseScreenDetector {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
}

export interface UseUiStore {
  modal: Modal;
  videoDownloaded: boolean;
  loading: boolean;
  onSetVideoDownloaded: (boolean: boolean) => void;
  onSetLoading: (boolean: boolean) => void;
  onOpenModal: (modal: Modal) => void;
  onResetModal: () => void;
}

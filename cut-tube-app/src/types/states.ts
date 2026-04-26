import type { Modal } from "@/types/app";

export interface UiState {
  loading: boolean;
  modal: Modal;
  videoDownloaded: boolean;
}

import type { PayloadAction } from "@reduxjs/toolkit";
import { createSlice } from "@reduxjs/toolkit";

import type { UiState } from "@/types/states";
import type { Modal } from "@/types/app";

const uiState: UiState = {
  loading: false,
  modal: {
    title: "",
    message: "",
    buttonText: "",
    open: false,
  },
  videoDownloaded: false,
};

export const uiSlice = createSlice({
  name: "ui",
  initialState: uiState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      const boolean = action.payload;

      state.loading = boolean;
    },
    setModal: (state, action: PayloadAction<Modal>) => {
      const modal = action.payload;

      state.modal = modal;
    },
    resetModal: (state) => {
      state.modal = { buttonText: "", message: "", open: false, title: "" };
    },
    setVideoDownloaded: (state, action: PayloadAction<boolean>) => {
      const boolean = action.payload;

      state.videoDownloaded = boolean;
    },
  },
});

export const { setLoading, setModal, resetModal, setVideoDownloaded } = uiSlice.actions;

export default uiSlice.reducer;

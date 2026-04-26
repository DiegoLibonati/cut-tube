import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { configureStore } from "@reduxjs/toolkit";
import { Provider } from "react-redux";

import type { RenderResult } from "@testing-library/react";
import type { UiState } from "@/types/states";
import type { store } from "@/app/store";

import VideoClippedView from "@/views/VideoClippedView/VideoClippedView";

import uiReducer from "@/features/ui/uiSlice";

const defaultUiState: UiState = {
  loading: false,
  modal: { title: "", message: "", buttonText: "", open: false },
  videoDownloaded: true,
};

const createTestStore = (uiState: Partial<UiState> = {}): typeof store =>
  configureStore({
    reducer: { ui: uiReducer },
    preloadedState: {
      ui: { ...defaultUiState, ...uiState },
    },
  });

const renderView = (uiState: Partial<UiState> = {}): RenderResult =>
  render(
    <Provider store={createTestStore(uiState)}>
      <VideoClippedView />
    </Provider>
  );

describe("VideoClippedView", () => {
  describe("rendering", () => {
    it("should render the congratulations heading", () => {
      renderView();
      expect(
        screen.getByRole("heading", { name: "Congratulations on creating your clip!" })
      ).toBeInTheDocument();
    });

    it("should render the description text", () => {
      renderView();
      expect(screen.getByText(/Your clip is being processed/i)).toBeInTheDocument();
    });

    it("should render the go back button", () => {
      renderView();
      expect(screen.getByRole("button", { name: "Go back to clip creation" })).toBeInTheDocument();
    });

    it("should render a main element", () => {
      renderView();
      expect(screen.getByRole("main")).toBeInTheDocument();
    });
  });

  describe("behavior", () => {
    it("should dispatch setVideoDownloaded(false) when Go back is clicked", async () => {
      const user = userEvent.setup();
      const store = createTestStore();
      render(
        <Provider store={store}>
          <VideoClippedView />
        </Provider>
      );
      await user.click(screen.getByRole("button", { name: "Go back to clip creation" }));
      expect(store.getState().ui.videoDownloaded).toBe(false);
    });
  });
});

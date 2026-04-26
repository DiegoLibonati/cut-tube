import { render, screen } from "@testing-library/react";
import { configureStore } from "@reduxjs/toolkit";
import { Provider } from "react-redux";

import type { RenderResult } from "@testing-library/react";
import type { UiState } from "@/types/states";
import type { store } from "@/app/store";

import CutPage from "@/pages/CutPage/CutPage";

import uiReducer from "@/features/ui/uiSlice";

const defaultUiState: UiState = {
  loading: false,
  modal: { title: "", message: "", buttonText: "", open: false },
  videoDownloaded: false,
};

const createTestStore = (uiState: Partial<UiState> = {}): typeof store =>
  configureStore({
    reducer: { ui: uiReducer },
    preloadedState: {
      ui: { ...defaultUiState, ...uiState },
    },
  });

const renderPage = (uiState: Partial<UiState> = {}): RenderResult =>
  render(
    <Provider store={createTestStore(uiState)}>
      <CutPage />
    </Provider>
  );

describe("CutPage", () => {
  beforeEach(() => {
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 375,
    });
  });

  describe("rendering", () => {
    it("should render CreateClipView by default", () => {
      renderPage();
      expect(screen.getByRole("form", { name: "Clip creation form" })).toBeInTheDocument();
    });

    it("should render LoadingView when loading is true", () => {
      renderPage({ loading: true });
      expect(screen.getByRole("status", { name: "Processing video clip" })).toBeInTheDocument();
    });

    it("should render VideoClippedView when videoDownloaded is true", () => {
      renderPage({ videoDownloaded: true });
      expect(
        screen.getByRole("heading", { name: "Congratulations on creating your clip!" })
      ).toBeInTheDocument();
    });

    it("should render Modal when modal is open", () => {
      renderPage({
        modal: { title: "Error", message: "Something went wrong", buttonText: "OK", open: true },
      });
      expect(screen.getByRole("dialog")).toBeInTheDocument();
    });

    it("should not render Modal when modal is closed", () => {
      renderPage({ modal: { title: "", message: "", buttonText: "", open: false } });
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    });

    it("should render NavBar on mobile screens", () => {
      Object.defineProperty(window, "innerWidth", {
        writable: true,
        configurable: true,
        value: 375,
      });
      renderPage();
      expect(screen.getByRole("banner")).toBeInTheDocument();
    });

    it("should render SideNav on desktop screens", () => {
      Object.defineProperty(window, "innerWidth", {
        writable: true,
        configurable: true,
        value: 1440,
      });
      renderPage();
      expect(screen.getByRole("complementary")).toBeInTheDocument();
    });

    it("should render SideNav on tablet screens", () => {
      Object.defineProperty(window, "innerWidth", {
        writable: true,
        configurable: true,
        value: 900,
      });
      renderPage();
      expect(screen.getByRole("complementary")).toBeInTheDocument();
    });

    it("should not render SideNav on mobile screens", () => {
      Object.defineProperty(window, "innerWidth", {
        writable: true,
        configurable: true,
        value: 375,
      });
      renderPage();
      expect(screen.queryByRole("complementary")).not.toBeInTheDocument();
    });
  });
});

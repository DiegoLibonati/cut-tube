import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { configureStore } from "@reduxjs/toolkit";
import { Provider } from "react-redux";

import type { RenderResult } from "@testing-library/react";
import type { UiState } from "@/types/states";
import type { store } from "@/app/store";

import Modal from "@/components/Modal/Modal";

import uiReducer from "@/features/ui/uiSlice";

const defaultUiState: UiState = {
  loading: false,
  modal: {
    title: "Test Title",
    message: "Test Message",
    buttonText: "Close",
    open: true,
  },
  videoDownloaded: false,
};

const createTestStore = (uiState: Partial<UiState> = {}): typeof store =>
  configureStore({
    reducer: { ui: uiReducer },
    preloadedState: {
      ui: { ...defaultUiState, ...uiState },
    },
  });

const renderComponent = (uiState: Partial<UiState> = {}): RenderResult => {
  const store = createTestStore(uiState);
  return render(
    <Provider store={store}>
      <Modal />
    </Provider>
  );
};

describe("Modal", () => {
  describe("rendering", () => {
    it("should render with the dialog role", () => {
      renderComponent();
      expect(screen.getByRole("dialog")).toBeInTheDocument();
    });

    it("should have aria-modal attribute set to true", () => {
      renderComponent();
      expect(screen.getByRole("dialog")).toHaveAttribute("aria-modal", "true");
    });

    it("should have the correct aria-labelledby", () => {
      renderComponent();
      expect(screen.getByRole("dialog")).toHaveAttribute("aria-labelledby", "modal-title");
    });

    it("should have the correct aria-describedby", () => {
      renderComponent();
      expect(screen.getByRole("dialog")).toHaveAttribute("aria-describedby", "modal-message");
    });

    it("should render the title from the store", () => {
      renderComponent({
        modal: { title: "Error", message: "Something failed", buttonText: "OK", open: true },
      });
      expect(screen.getByRole("heading", { name: "Error" })).toBeInTheDocument();
    });

    it("should render the message from the store", () => {
      renderComponent({
        modal: { title: "Info", message: "Operation successful", buttonText: "Done", open: true },
      });
      expect(screen.getByText("Operation successful")).toBeInTheDocument();
    });

    it("should render the button with correct accessible name", () => {
      renderComponent();
      expect(screen.getByRole("button", { name: "Close modal" })).toBeInTheDocument();
    });

    it("should render the button text from the store", () => {
      renderComponent({
        modal: { title: "Alert", message: "Warning", buttonText: "Dismiss", open: true },
      });
      expect(screen.getByRole("button", { name: "Close modal" })).toHaveTextContent("Dismiss");
    });
  });

  describe("behavior", () => {
    it("should dispatch resetModal when close button is clicked", async () => {
      const user = userEvent.setup();
      const store = createTestStore();
      render(
        <Provider store={store}>
          <Modal />
        </Provider>
      );
      await user.click(screen.getByRole("button", { name: "Close modal" }));
      expect(store.getState().ui.modal.open).toBe(false);
      expect(store.getState().ui.modal.title).toBe("");
      expect(store.getState().ui.modal.message).toBe("");
    });
  });
});

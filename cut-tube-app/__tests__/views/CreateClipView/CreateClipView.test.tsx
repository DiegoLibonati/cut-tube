import { act, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { configureStore } from "@reduxjs/toolkit";
import { Provider } from "react-redux";

import type { RenderResult } from "@testing-library/react";
import type { store } from "@/app/store";

import CreateClipView from "@/views/CreateClipView/CreateClipView";

import uiReducer from "@/features/ui/uiSlice";

const mockClipVideo: jest.Mock = jest.requireMock("@/services/cutTubeService").default.clipVideo;
const mockRemoveClip: jest.Mock = jest.requireMock("@/services/cutTubeService").default.removeClip;

jest.mock("@/services/cutTubeService", () => ({
  __esModule: true,
  default: {
    clipVideo: jest.fn(),
    removeClip: jest.fn(),
  },
}));

const createTestStore = (): typeof store =>
  configureStore({
    reducer: { ui: uiReducer },
  });

const renderView = (): RenderResult =>
  render(
    <Provider store={createTestStore()}>
      <CreateClipView />
    </Provider>
  );

describe("CreateClipView", () => {
  describe("rendering", () => {
    it("should render the Cut Tube heading", () => {
      renderView();
      expect(screen.getByRole("heading", { name: "Cut Tube" })).toBeInTheDocument();
    });

    it("should render the clip creation form", () => {
      renderView();
      expect(screen.getByRole("form", { name: "Clip creation form" })).toBeInTheDocument();
    });

    it("should render the Start Time input", () => {
      renderView();
      expect(screen.getByRole("textbox", { name: "Start Time" })).toBeInTheDocument();
    });

    it("should render the End Time input", () => {
      renderView();
      expect(screen.getByRole("textbox", { name: "End Time" })).toBeInTheDocument();
    });

    it("should render the Clip Title input", () => {
      renderView();
      expect(screen.getByRole("textbox", { name: "Clip Title" })).toBeInTheDocument();
    });

    it("should render the YouTube Link input", () => {
      renderView();
      expect(screen.getByRole("textbox", { name: "YouTube Link" })).toBeInTheDocument();
    });

    it("should render the submit button", () => {
      renderView();
      expect(screen.getByRole("button", { name: "Submit clip creation" })).toBeInTheDocument();
    });

    it("should render inputs with correct placeholders", () => {
      renderView();
      expect(screen.getAllByPlaceholderText("00:00:00")).toHaveLength(2);
    });
  });

  describe("behavior", () => {
    it("should update Start Time input when user types", async () => {
      const user = userEvent.setup();
      renderView();
      const input = screen.getByRole("textbox", { name: "Start Time" });
      await user.type(input, "00:00:10");
      expect(input).toHaveValue("00:00:10");
    });

    it("should update Clip Title input when user types", async () => {
      const user = userEvent.setup();
      renderView();
      const input = screen.getByRole("textbox", { name: "Clip Title" });
      await user.type(input, "my_clip");
      expect(input).toHaveValue("my_clip");
    });

    it("should set modal open when submitting with all empty fields", async () => {
      const user = userEvent.setup();
      const store = createTestStore();
      render(
        <Provider store={store}>
          <CreateClipView />
        </Provider>
      );
      await user.click(screen.getByRole("button", { name: "Submit clip creation" }));
      await waitFor(() => {
        expect(store.getState().ui.modal.open).toBe(true);
      });
    });

    it("should set error message for empty fields", async () => {
      const user = userEvent.setup();
      const store = createTestStore();
      render(
        <Provider store={store}>
          <CreateClipView />
        </Provider>
      );
      await user.click(screen.getByRole("button", { name: "Submit clip creation" }));
      await waitFor(() => {
        expect(store.getState().ui.modal.message).toBe("You cannot have empty values");
      });
    });

    it("should set modal open when submitting with invalid time format", async () => {
      const user = userEvent.setup();
      const store = createTestStore();
      render(
        <Provider store={store}>
          <CreateClipView />
        </Provider>
      );
      await user.type(screen.getByRole("textbox", { name: "Start Time" }), "10:00");
      await user.type(screen.getByRole("textbox", { name: "End Time" }), "20:00");
      await user.type(screen.getByRole("textbox", { name: "Clip Title" }), "my_clip");
      await user.type(screen.getByRole("textbox", { name: "YouTube Link" }), "https://youtube.com");
      await user.click(screen.getByRole("button", { name: "Submit clip creation" }));
      await waitFor(() => {
        expect(store.getState().ui.modal.open).toBe(true);
      });
    });

    it("should set time format error message when time is invalid", async () => {
      const user = userEvent.setup();
      const store = createTestStore();
      render(
        <Provider store={store}>
          <CreateClipView />
        </Provider>
      );
      await user.type(screen.getByRole("textbox", { name: "Start Time" }), "10:00");
      await user.type(screen.getByRole("textbox", { name: "End Time" }), "20:00");
      await user.type(screen.getByRole("textbox", { name: "Clip Title" }), "my_clip");
      await user.type(screen.getByRole("textbox", { name: "YouTube Link" }), "https://youtube.com");
      await user.click(screen.getByRole("button", { name: "Submit clip creation" }));
      await waitFor(() => {
        expect(store.getState().ui.modal.message).toContain("valid format");
      });
    });

    it("should call clipVideo with correct form data on valid submission", async () => {
      jest.useFakeTimers();
      jest.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {
        // Empty fn
      });
      const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
      mockClipVideo.mockResolvedValue({
        code: "SUCCESS_CUT_VIDEO",
        message: "Video cutted.",
        data: { name: "my_clip.mp4", filename: "my_clip" },
      });
      mockRemoveClip.mockResolvedValue({ code: "SUCCESS_DELETE_CLIP", message: "Clip deleted." });
      renderView();
      await user.type(screen.getByRole("textbox", { name: "Start Time" }), "00:00:10");
      await user.type(screen.getByRole("textbox", { name: "End Time" }), "00:00:20");
      await user.type(screen.getByRole("textbox", { name: "Clip Title" }), "my_clip");
      await user.type(
        screen.getByRole("textbox", { name: "YouTube Link" }),
        "https://youtube.com/watch?v=abc123"
      );
      await user.click(screen.getByRole("button", { name: "Submit clip creation" }));
      await waitFor(() => {
        expect(mockClipVideo).toHaveBeenCalledWith({
          start: "00:00:10",
          end: "00:00:20",
          filename: "my_clip",
          url: "https://youtube.com/watch?v=abc123",
        });
      });
      await act(async () => {
        await jest.runAllTimersAsync();
      });
      jest.useRealTimers();
    });

    it("should set modal open when clipVideo throws an error", async () => {
      const user = userEvent.setup();
      const store = createTestStore();
      mockClipVideo.mockRejectedValue(new Error("Server error"));
      render(
        <Provider store={store}>
          <CreateClipView />
        </Provider>
      );
      await user.type(screen.getByRole("textbox", { name: "Start Time" }), "00:00:10");
      await user.type(screen.getByRole("textbox", { name: "End Time" }), "00:00:20");
      await user.type(screen.getByRole("textbox", { name: "Clip Title" }), "my_clip");
      await user.type(
        screen.getByRole("textbox", { name: "YouTube Link" }),
        "https://youtube.com/watch?v=abc123"
      );
      await user.click(screen.getByRole("button", { name: "Submit clip creation" }));
      await waitFor(() => {
        expect(store.getState().ui.modal.open).toBe(true);
      });
    });
  });
});

import { render, screen } from "@testing-library/react";

import type { RenderResult } from "@testing-library/react";

import LoadingView from "@/views/LoadingView/LoadingView";

const renderView = (): RenderResult => render(<LoadingView />);

describe("LoadingView", () => {
  describe("rendering", () => {
    it("should render the loader", () => {
      renderView();
      expect(screen.getByRole("status", { name: "Processing video clip" })).toBeInTheDocument();
    });

    it("should render the processing message", () => {
      renderView();
      expect(screen.getByText(/Your video clip is being processed/i)).toBeInTheDocument();
    });

    it("should render a main element", () => {
      renderView();
      expect(screen.getByRole("main")).toBeInTheDocument();
    });
  });
});

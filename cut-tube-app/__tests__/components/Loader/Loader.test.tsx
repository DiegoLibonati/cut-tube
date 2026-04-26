import { render, screen } from "@testing-library/react";

import type { RenderResult } from "@testing-library/react";

import Loader from "@/components/Loader/Loader";

const renderComponent = (): RenderResult => render(<Loader />);

describe("Loader", () => {
  describe("rendering", () => {
    it("should render the loader element", () => {
      renderComponent();
      expect(screen.getByRole("status")).toBeInTheDocument();
    });

    it("should have the correct aria-label", () => {
      renderComponent();
      expect(screen.getByRole("status")).toHaveAttribute("aria-label", "Processing video clip");
    });

    it("should have the loader class", () => {
      renderComponent();
      expect(screen.getByRole("status")).toHaveClass("loader");
    });
  });
});

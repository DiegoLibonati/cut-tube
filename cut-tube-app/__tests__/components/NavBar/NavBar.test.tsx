import { render, screen } from "@testing-library/react";

import type { RenderResult } from "@testing-library/react";

import NavBar from "@/components/NavBar/NavBar";

const renderComponent = (): RenderResult => render(<NavBar />);

describe("NavBar", () => {
  describe("rendering", () => {
    it("should render a header element", () => {
      renderComponent();
      expect(screen.getByRole("banner")).toBeInTheDocument();
    });

    it("should render the logo with the correct aria-label", () => {
      renderComponent();
      expect(screen.getByRole("img", { name: "Cut Tube logo" })).toBeInTheDocument();
    });
  });
});

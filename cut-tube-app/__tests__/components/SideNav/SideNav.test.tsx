import { render, screen } from "@testing-library/react";

import type { RenderResult } from "@testing-library/react";

import SideNav from "@/components/SideNav/SideNav";

const renderComponent = (): RenderResult => render(<SideNav />);

describe("SideNav", () => {
  describe("rendering", () => {
    it("should render an aside element", () => {
      renderComponent();
      expect(screen.getByRole("complementary")).toBeInTheDocument();
    });

    it("should render the create clip button", () => {
      renderComponent();
      expect(
        screen.getByRole("button", { name: "Navigate to create a new clip" })
      ).toBeInTheDocument();
    });

    it("should render the Create clip label text", () => {
      renderComponent();
      expect(screen.getByText("Create clip")).toBeInTheDocument();
    });
  });
});

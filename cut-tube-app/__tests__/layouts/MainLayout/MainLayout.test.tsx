import { render, screen } from "@testing-library/react";

import type { RenderResult } from "@testing-library/react";
import type { MainLayoutProps } from "@/types/props";

import MainLayout from "@/layouts/MainLayout/MainLayout";

const renderComponent = (props: Partial<MainLayoutProps> = {}): RenderResult => {
  const defaultProps: MainLayoutProps = {
    children: <span>content</span>,
    className: undefined!,
    ...props,
  };
  return render(<MainLayout {...defaultProps} />);
};

describe("MainLayout", () => {
  describe("rendering", () => {
    it("should render a main element", () => {
      renderComponent();
      expect(screen.getByRole("main")).toBeInTheDocument();
    });

    it("should render its children", () => {
      renderComponent({ children: <span>hello layout</span> });
      expect(screen.getByText("hello layout")).toBeInTheDocument();
    });

    it("should always apply the base classes", () => {
      renderComponent();
      const main = screen.getByRole("main");
      expect(main).toHaveClass("w-full");
      expect(main).toHaveClass("min-h-screen");
      expect(main).toHaveClass("bg-primary");
    });

    it("should apply additional className when provided", () => {
      renderComponent({ className: "flex items-center" });
      expect(screen.getByRole("main")).toHaveClass("flex", "items-center");
    });

    it("should render without additional class when className is not provided", () => {
      renderComponent({ className: undefined! });
      const main = screen.getByRole("main");
      expect(main).toHaveClass("w-full");
    });
  });
});

import { render, screen } from "@testing-library/react";

import type { RenderResult } from "@testing-library/react";
import type { InputRootProps } from "@/types/props";

import InputRoot from "@/components/InputRoot/InputRoot";

const renderComponent = (props: Partial<InputRootProps> = {}): RenderResult => {
  const defaultProps: InputRootProps = {
    children: <span>child content</span>,
    className: "test-class",
    ...props,
  };
  return render(<InputRoot {...defaultProps} />);
};

describe("InputRoot", () => {
  describe("rendering", () => {
    it("should render its children", () => {
      renderComponent({ children: <span>hello</span> });
      expect(screen.getByText("hello")).toBeInTheDocument();
    });

    it("should apply the provided className", () => {
      const { container } = renderComponent({ className: "my-root" });
      expect(container.firstChild).toHaveClass("my-root");
    });

    it("should render as a div", () => {
      const { container } = renderComponent();
      expect(container.firstChild?.nodeName).toBe("DIV");
    });

    it("should render multiple children", () => {
      renderComponent({
        children: (
          <>
            <span>first</span>
            <span>second</span>
          </>
        ),
      });
      expect(screen.getByText("first")).toBeInTheDocument();
      expect(screen.getByText("second")).toBeInTheDocument();
    });
  });
});

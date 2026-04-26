import { render, screen } from "@testing-library/react";

import type { RenderResult } from "@testing-library/react";
import type { LabelProps } from "@/types/props";

import Label from "@/components/Label/Label";

const renderComponent = (props: Partial<LabelProps> = {}): RenderResult => {
  const defaultProps: LabelProps = {
    labelText: "Default Label",
    htmlFor: "input-id",
    className: "label-class",
    ...props,
  };
  return render(<Label {...defaultProps} />);
};

describe("Label", () => {
  describe("rendering", () => {
    it("should render the label text", () => {
      renderComponent({ labelText: "Username" });
      expect(screen.getByText("Username")).toBeInTheDocument();
    });

    it("should render as a label element", () => {
      renderComponent();
      expect(screen.getByText("Default Label").tagName).toBe("LABEL");
    });

    it("should render with the correct htmlFor attribute", () => {
      renderComponent({ htmlFor: "my-input" });
      expect(screen.getByText("Default Label")).toHaveAttribute("for", "my-input");
    });

    it("should apply the provided className", () => {
      renderComponent({ className: "custom-class" });
      expect(screen.getByText("Default Label")).toHaveClass("custom-class");
    });
  });
});

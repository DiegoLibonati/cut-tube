import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { RenderResult } from "@testing-library/react";
import type { InputProps } from "@/types/props";

import Input from "@/components/Input/Input";

const mockOnChange = jest.fn();

const renderComponent = (props: Partial<InputProps> = {}): RenderResult => {
  const defaultProps: InputProps = {
    id: "test-input",
    type: "text",
    className: "test-class",
    placeholder: "Enter value",
    value: "",
    name: "test-name",
    onChange: mockOnChange,
    ...props,
  };
  return render(<Input {...defaultProps} />);
};

describe("Input", () => {
  describe("rendering", () => {
    it("should render the input element", () => {
      renderComponent();
      expect(screen.getByRole("textbox")).toBeInTheDocument();
    });

    it("should render with the correct id", () => {
      renderComponent({ id: "my-input" });
      expect(screen.getByRole("textbox")).toHaveAttribute("id", "my-input");
    });

    it("should render with the correct placeholder", () => {
      renderComponent({ placeholder: "Type here" });
      expect(screen.getByPlaceholderText("Type here")).toBeInTheDocument();
    });

    it("should render with the correct value", () => {
      renderComponent({ value: "hello" });
      expect(screen.getByRole("textbox")).toHaveValue("hello");
    });

    it("should render with the correct name attribute", () => {
      renderComponent({ name: "email-field" });
      expect(screen.getByRole("textbox")).toHaveAttribute("name", "email-field");
    });

    it("should render with the provided className", () => {
      renderComponent({ className: "my-class" });
      expect(screen.getByRole("textbox")).toHaveClass("my-class");
    });

    it("should render with the correct type attribute", () => {
      renderComponent({ type: "text" });
      expect(screen.getByRole("textbox")).toHaveAttribute("type", "text");
    });
  });

  describe("behavior", () => {
    it("should call onChange when user types", async () => {
      const user = userEvent.setup();
      renderComponent({ value: "" });
      await user.type(screen.getByRole("textbox"), "a");
      expect(mockOnChange).toHaveBeenCalled();
    });

    it("should call onChange with the correct event target name", async () => {
      const user = userEvent.setup();
      renderComponent({ name: "start", value: "" });
      await user.type(screen.getByRole("textbox"), "a");
      const event = mockOnChange.mock.calls[0][0] as React.ChangeEvent<HTMLInputElement>;
      expect(event.target.name).toBe("start");
    });
  });
});

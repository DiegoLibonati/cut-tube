import type { JSX } from "react";
import type { LabelProps } from "@/types/props";

const Label = ({ labelText, htmlFor, className }: LabelProps): JSX.Element => {
  return (
    <label className={className} htmlFor={htmlFor}>
      {labelText}
    </label>
  );
};

export default Label;

import type { JSX } from "react";
import type { InputRootProps } from "@/types/props";

const InputRoot = ({ children, className }: InputRootProps): JSX.Element => {
  return <div className={className}>{children}</div>;
};

export default InputRoot;

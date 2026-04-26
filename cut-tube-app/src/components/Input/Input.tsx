import type { JSX } from "react";
import type { InputProps } from "@/types/props";

const Input = ({
  id,
  type,
  className,
  placeholder,
  value,
  name,
  onChange,
}: InputProps): JSX.Element => {
  return (
    <input
      id={id}
      type={type}
      className={className}
      placeholder={placeholder}
      value={value}
      name={name}
      onChange={onChange}
    ></input>
  );
};

export default Input;

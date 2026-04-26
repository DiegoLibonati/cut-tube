import type { JSX } from "react";
import type { MainLayoutProps } from "@/types/props";

const MainLayout = ({ children, className }: MainLayoutProps): JSX.Element => {
  return <main className={`w-full min-h-screen bg-primary ${className}`}>{children}</main>;
};

export default MainLayout;

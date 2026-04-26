import type { JSX } from "react";

import "@/components/Loader/Loader.css";

const Loader = (): JSX.Element => {
  return <div className="loader" role="status" aria-label="Processing video clip"></div>;
};

export default Loader;

import { HashRouter } from "react-router-dom";

import type { JSX } from "react";

import { CutTubeRouter } from "@/router/CutTubeRouter";

function App(): JSX.Element {
  return (
    <HashRouter>
      <CutTubeRouter></CutTubeRouter>
    </HashRouter>
  );
}

export default App;

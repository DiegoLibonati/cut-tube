import { useEffect, useState } from "react";

import type { UseScreenDetector } from "@/types/hooks";

export const useScreenDetector = (): UseScreenDetector => {
  const [width, setWidth] = useState(window.innerWidth);

  const handleWindowSizeChange = (): void => {
    setWidth(window.innerWidth);
  };

  useEffect(() => {
    window.addEventListener("resize", handleWindowSizeChange);

    return (): void => {
      window.removeEventListener("resize", handleWindowSizeChange);
    };
  }, []);

  return {
    isMobile: width <= 768,
    isTablet: width > 768 && width <= 1024,
    isDesktop: width > 1024,
  };
};

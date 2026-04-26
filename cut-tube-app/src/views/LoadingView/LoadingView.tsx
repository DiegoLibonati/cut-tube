import type { JSX } from "react";

import Loader from "@/components/Loader/Loader";

import MainLayout from "@/layouts/MainLayout/MainLayout";

const LoadingView = (): JSX.Element => {
  return (
    <MainLayout className="flex flex-col items-center justify-center">
      <Loader></Loader>
      <h2 className="text-white text-base mt-4 font-semibold w-[75%] text-center">
        Your video clip is being processed. This may take a few moments
      </h2>
    </MainLayout>
  );
};

export default LoadingView;

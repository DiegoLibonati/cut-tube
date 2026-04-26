import { BiCheckCircle } from "react-icons/bi";
import { PiPencil } from "react-icons/pi";
import { SlStar } from "react-icons/sl";

import type { JSX } from "react";

import MainLayout from "@/layouts/MainLayout/MainLayout";

import { useUiStore } from "@/hooks/useUiStore";

const VideoClippedView = (): JSX.Element => {
  const { onSetVideoDownloaded } = useUiStore();

  const handleClickGoBack: React.MouseEventHandler<HTMLButtonElement> = () => {
    onSetVideoDownloaded(false);
  };

  return (
    <MainLayout className="flex flex-col items-center justify-center">
      <div className="relative" aria-hidden="true">
        <SlStar className="absolute text-[2rem] -top-18 -left-12" fill="white"></SlStar>
        <PiPencil fill="white" className="absolute text-[4rem] -top-12 left-28"></PiPencil>
        <BiCheckCircle fill="white" className="text-[8rem]"></BiCheckCircle>
      </div>

      <h2 className="text-white text-xl font-semibold mt-4">
        Congratulations on creating your clip!
      </h2>

      <p className="text-white text-base mt-2 text-center">
        Your clip is being processed and will be ready shortly.
      </p>

      <button
        type="button"
        className="text-white bg-secondary p-2 w-[15rem] rounded-full mt-48"
        aria-label="Go back to clip creation"
        onClick={handleClickGoBack}
      >
        Go back
      </button>
    </MainLayout>
  );
};

export default VideoClippedView;

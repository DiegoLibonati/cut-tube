import type { JSX } from "react";

import Modal from "@/components/Modal/Modal";
import NavBar from "@/components/NavBar/NavBar";
import SideNav from "@/components/SideNav/SideNav";

import CreateClipView from "@/views/CreateClipView/CreateClipView";
import LoadingView from "@/views/LoadingView/LoadingView";
import VideoClippedView from "@/views/VideoClippedView/VideoClippedView";

import { useUiStore } from "@/hooks/useUiStore";
import { useScreenDetector } from "@/hooks/useScreenDetector";

const CutPage = (): JSX.Element => {
  const { isTablet, isDesktop } = useScreenDetector();
  const { modal, loading, videoDownloaded } = useUiStore();

  return (
    <div className={`flex w-full min-h-screen`}>
      {isTablet || isDesktop ? <SideNav></SideNav> : <NavBar></NavBar>}

      {loading ? (
        <LoadingView></LoadingView>
      ) : videoDownloaded ? (
        <VideoClippedView></VideoClippedView>
      ) : (
        <CreateClipView></CreateClipView>
      )}

      {modal.open && <Modal></Modal>}
    </div>
  );
};

export default CutPage;

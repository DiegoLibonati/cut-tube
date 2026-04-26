import type { JSX } from "react";

import { useUiStore } from "@/hooks/useUiStore";

const Modal = (): JSX.Element => {
  const { modal, onResetModal } = useUiStore();

  const handleClickButton: React.MouseEventHandler<HTMLButtonElement> = () => {
    onResetModal();
  };

  return (
    <div
      className="flex items-center justify-center absolute bg-black bg-opacity-75 w-full h-full"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      aria-describedby="modal-message"
    >
      <div className="flex flex-col items-center justify-around bg-charcoal w-[22rem] h-[12.5rem] p-4 rounded-lg shadow-md">
        <h2 id="modal-title" className="text-xl font-semibold text-white">
          {modal.title}
        </h2>
        <p id="modal-message" className="text-white text-center text-base">
          {modal.message}
        </p>
        <button
          className="text-white rounded-lg bg-black p-2 cursor-pointer"
          type="button"
          aria-label="Close modal"
          onClick={handleClickButton}
        >
          {modal.buttonText}
        </button>
      </div>
    </div>
  );
};

export default Modal;

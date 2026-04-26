import { isAxiosError } from "axios";

import type { FormClip } from "@/types/forms";

import cutTubeService from "@/services/cutTubeService";

const mockApiDelete: jest.Mock = jest.requireMock("@/services/axios").apiCutTube.delete;
const mockApiPost: jest.Mock = jest.requireMock("@/services/axios").apiCutTube.post;
const mockIsAxiosError = jest.mocked(isAxiosError);

const mockClipResponse = {
  code: "SUCCESS_CUT_VIDEO",
  message: "Video cutted.",
  data: { name: "my_clip_uuid.mp4", filename: "my_clip_uuid" },
};
const mockDeleteResponse = {
  code: "SUCCESS_DELETE_CLIP",
  message: "Clip deleted.",
};

jest.mock("axios");
jest.mock("@/services/axios", () => ({
  apiCutTube: {
    delete: jest.fn(),
    post: jest.fn(),
  },
}));

const mockAxiosSuccess = (method: jest.Mock, data: unknown): void => {
  method.mockResolvedValue({ data });
};

const mockAxiosError = (method: jest.Mock, status: number | undefined, message: string): void => {
  method.mockRejectedValue({
    response: status !== undefined ? { status } : undefined,
    message,
  });
  mockIsAxiosError.mockReturnValue(true);
};

const mockAxiosNetworkError = (method: jest.Mock, message = "Network error"): void => {
  method.mockRejectedValue(new Error(message));
  mockIsAxiosError.mockReturnValue(false);
};

const mockForm: FormClip = {
  filename: "my_clip",
  start: "00:00:10",
  end: "00:00:20",
  url: "https://www.youtube.com/watch?v=abc123",
};

describe("cutTubeService", () => {
  describe("clipVideo", () => {
    describe("when the request succeeds", () => {
      it("should return the clip response data", async () => {
        mockAxiosSuccess(mockApiPost, mockClipResponse);
        const result = await cutTubeService.clipVideo(mockForm);
        expect(result).toEqual(mockClipResponse);
      });

      it("should call the correct endpoint with the filename", async () => {
        mockAxiosSuccess(mockApiPost, mockClipResponse);
        await cutTubeService.clipVideo(mockForm);
        expect(mockApiPost).toHaveBeenCalledWith("/my_clip/clip", expect.any(String));
      });

      it("should send the correct JSON body", async () => {
        mockAxiosSuccess(mockApiPost, mockClipResponse);
        await cutTubeService.clipVideo(mockForm);
        const body = JSON.parse(mockApiPost.mock.calls[0][1] as string) as Record<string, string>;
        expect(body).toEqual({
          url: mockForm.url,
          start: mockForm.start,
          end: mockForm.end,
        });
      });
    });

    describe("when the server returns an HTTP error", () => {
      it("should throw an error containing the status code", async () => {
        mockAxiosError(mockApiPost, 409, "Conflict");
        await expect(cutTubeService.clipVideo(mockForm)).rejects.toThrow("409");
      });

      it("should throw an error when status is undefined", async () => {
        mockAxiosError(mockApiPost, undefined, "Unknown error");
        await expect(cutTubeService.clipVideo(mockForm)).rejects.toThrow("HTTP error!");
      });

      it("should throw an Error instance", async () => {
        mockAxiosError(mockApiPost, 500, "Server Error");
        await expect(cutTubeService.clipVideo(mockForm)).rejects.toBeInstanceOf(Error);
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockAxiosNetworkError(mockApiPost, "Network error");
        await expect(cutTubeService.clipVideo(mockForm)).rejects.toThrow("Network error");
      });
    });
  });

  describe("removeClip", () => {
    describe("when the request succeeds", () => {
      it("should return the delete response data", async () => {
        mockAxiosSuccess(mockApiDelete, mockDeleteResponse);
        const result = await cutTubeService.removeClip("my_clip");
        expect(result).toEqual(mockDeleteResponse);
      });

      it("should call the correct endpoint with the filename", async () => {
        mockAxiosSuccess(mockApiDelete, mockDeleteResponse);
        await cutTubeService.removeClip("my_clip");
        expect(mockApiDelete).toHaveBeenCalledWith("/my_clip");
      });

      it("should call the correct endpoint with a different filename", async () => {
        mockAxiosSuccess(mockApiDelete, mockDeleteResponse);
        await cutTubeService.removeClip("clip_abc_123");
        expect(mockApiDelete).toHaveBeenCalledWith("/clip_abc_123");
      });
    });

    describe("when the server returns an HTTP error", () => {
      it("should throw an error containing the status code", async () => {
        mockAxiosError(mockApiDelete, 404, "Not Found");
        await expect(cutTubeService.removeClip("nonexistent")).rejects.toThrow("404");
      });

      it("should throw an Error instance", async () => {
        mockAxiosError(mockApiDelete, 500, "Server Error");
        await expect(cutTubeService.removeClip("clip")).rejects.toBeInstanceOf(Error);
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockAxiosNetworkError(mockApiDelete, "Network error");
        await expect(cutTubeService.removeClip("clip")).rejects.toThrow("Network error");
      });
    });
  });
});

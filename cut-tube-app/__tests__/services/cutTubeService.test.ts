import { http, HttpResponse } from "msw";

import type { FormClip } from "@/types/forms";

import cutTubeService from "@/services/cutTubeService";

import { mockMswServer } from "@tests/__mocks__/mswServer.mock";

const mockForm: FormClip = {
  filename: "my_clip",
  start: "00:00:10",
  end: "00:00:20",
  url: "https://www.youtube.com/watch?v=abc123",
};

const mockClipResponse = {
  code: "SUCCESS_CUT_VIDEO",
  message: "Video cutted.",
  data: { name: "my_clip.mp4", filename: "my_clip" },
};

const mockDeleteResponse = {
  code: "SUCCESS_DELETE_CLIP",
  message: "Clip deleted.",
};

describe("cutTubeService", () => {
  describe("clipVideo", () => {
    describe("when the request succeeds", () => {
      it("should return the clip response data", async () => {
        const result = await cutTubeService.clipVideo(mockForm);

        expect(result).toEqual(mockClipResponse);
      });

      it("should call the correct endpoint with the filename", async () => {
        let calledUrl = "";
        mockMswServer.use(
          http.post("/api/v1/cut/:filename/clip", ({ request, params }) => {
            calledUrl = new URL(request.url).pathname;
            const filename = String(params.filename);
            return HttpResponse.json({
              code: "SUCCESS_CUT_VIDEO",
              message: "Video cutted.",
              data: { name: `${filename}.mp4`, filename },
            });
          })
        );

        await cutTubeService.clipVideo(mockForm);

        expect(calledUrl).toBe("/api/v1/cut/my_clip/clip");
      });

      it("should send the correct JSON body", async () => {
        let sentBody: Record<string, string> = {};
        mockMswServer.use(
          http.post("/api/v1/cut/:filename/clip", async ({ request, params }) => {
            sentBody = (await request.json()) as Record<string, string>;
            const filename = String(params.filename);
            return HttpResponse.json({
              code: "SUCCESS_CUT_VIDEO",
              message: "Video cutted.",
              data: { name: `${filename}.mp4`, filename },
            });
          })
        );

        await cutTubeService.clipVideo(mockForm);

        expect(sentBody).toEqual({
          url: mockForm.url,
          start: mockForm.start,
          end: mockForm.end,
        });
      });
    });

    describe("when the server returns an HTTP error", () => {
      it("should throw an error containing the status code", async () => {
        mockMswServer.use(
          http.post("/api/v1/cut/:filename/clip", () => {
            return new HttpResponse(null, { status: 409, statusText: "Conflict" });
          })
        );

        await expect(cutTubeService.clipVideo(mockForm)).rejects.toThrow("409");
      });

      it("should throw an Error instance on server error", async () => {
        mockMswServer.use(
          http.post("/api/v1/cut/:filename/clip", () => {
            return new HttpResponse(null, { status: 500 });
          })
        );

        await expect(cutTubeService.clipVideo(mockForm)).rejects.toBeInstanceOf(Error);
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockMswServer.use(
          http.post("/api/v1/cut/:filename/clip", () => {
            return HttpResponse.error();
          })
        );

        await expect(cutTubeService.clipVideo(mockForm)).rejects.toThrow();
      });
    });
  });

  describe("removeClip", () => {
    describe("when the request succeeds", () => {
      it("should return the delete response data", async () => {
        const result = await cutTubeService.removeClip("my_clip");

        expect(result).toEqual(mockDeleteResponse);
      });

      it("should call the correct endpoint with the filename", async () => {
        let calledUrl = "";
        mockMswServer.use(
          http.delete("/api/v1/cut/:filename", ({ request }) => {
            calledUrl = new URL(request.url).pathname;
            return HttpResponse.json(mockDeleteResponse);
          })
        );

        await cutTubeService.removeClip("my_clip");

        expect(calledUrl).toBe("/api/v1/cut/my_clip");
      });

      it("should call the correct endpoint with a different filename", async () => {
        let calledUrl = "";
        mockMswServer.use(
          http.delete("/api/v1/cut/:filename", ({ request }) => {
            calledUrl = new URL(request.url).pathname;
            return HttpResponse.json(mockDeleteResponse);
          })
        );

        await cutTubeService.removeClip("clip_abc_123");

        expect(calledUrl).toBe("/api/v1/cut/clip_abc_123");
      });
    });

    describe("when the server returns an HTTP error", () => {
      it("should throw an error containing the status code", async () => {
        mockMswServer.use(
          http.delete("/api/v1/cut/:filename", () => {
            return new HttpResponse(null, { status: 404, statusText: "Not Found" });
          })
        );

        await expect(cutTubeService.removeClip("nonexistent")).rejects.toThrow("404");
      });

      it("should throw an Error instance on server error", async () => {
        mockMswServer.use(
          http.delete("/api/v1/cut/:filename", () => {
            return new HttpResponse(null, { status: 500 });
          })
        );

        await expect(cutTubeService.removeClip("clip")).rejects.toBeInstanceOf(Error);
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockMswServer.use(
          http.delete("/api/v1/cut/:filename", () => {
            return HttpResponse.error();
          })
        );

        await expect(cutTubeService.removeClip("clip")).rejects.toThrow();
      });
    });
  });
});

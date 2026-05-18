import { http, HttpResponse } from "msw";

export const mockMswHandlers = [
  http.post("/api/v1/cut/:filename/clip", ({ params }) => {
    const filename = String(params.filename);
    return HttpResponse.json({
      code: "SUCCESS_CUT_VIDEO",
      message: "Video cutted.",
      data: {
        name: `${filename}.mp4`,
        filename,
      },
    });
  }),
  http.delete("/api/v1/cut/:filename", () => {
    return HttpResponse.json({
      code: "SUCCESS_DELETE_CLIP",
      message: "Clip deleted.",
    });
  }),
];

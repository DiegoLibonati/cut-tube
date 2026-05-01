import axios from "axios";

import type { FormClip } from "@/types/forms";
import type { DefaultResponse, ResponseWithData } from "@/types/responses";

import { apiCutTube } from "@/services/axios";

const cutTubeService = {
  removeClip: async (filename: string): Promise<DefaultResponse> => {
    try {
      const request = await apiCutTube.delete<DefaultResponse>(`/${filename}`);
      return request.data;
    } catch (e) {
      if (axios.isAxiosError(e)) {
        throw new Error(`HTTP error! status: ${e.response?.status} - ${e.message}`);
      }
      throw e;
    }
  },
  clipVideo: async (
    form: FormClip
  ): Promise<
    ResponseWithData<{
      name: string;
      filename: string;
    }>
  > => {
    try {
      const request = await apiCutTube.post<
        ResponseWithData<{
          name: string;
          filename: string;
        }>
      >(
        `/${form.filename}/clip`,
        JSON.stringify({
          url: form.url,
          start: form.start,
          end: form.end,
        })
      );
      return request.data;
    } catch (e) {
      if (axios.isAxiosError(e)) {
        throw new Error(`HTTP error! status: ${e.response?.status} - ${e.message}`);
      }
      throw e;
    }
  },
};

export default cutTubeService;

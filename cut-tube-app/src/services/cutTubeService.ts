import axios from "axios";

import type { FormClip } from "@/types/forms";

import { apiCutTube } from "@/services/axios";

const cutTubeService = {
  removeClip: async (
    filename: string
  ): Promise<{
    code: string;
    message: string;
  }> => {
    try {
      const request = await apiCutTube.delete(`/${filename}`);
      return request.data as {
        code: string;
        message: string;
      };
    } catch (e) {
      if (axios.isAxiosError(e)) {
        throw new Error(`HTTP error! status: ${e.response?.status} - ${e.message}`);
      }
      throw e;
    }
  },
  clipVideo: async (
    form: FormClip
  ): Promise<{
    code: string;
    message: string;
    data: {
      name: string;
      filename: string;
    };
  }> => {
    try {
      const request = await apiCutTube.post(
        `/${form.filename}/clip`,
        JSON.stringify({
          url: form.url,
          start: form.start,
          end: form.end,
        })
      );
      return request.data as {
        code: string;
        message: string;
        data: {
          name: string;
          filename: string;
        };
      };
    } catch (e) {
      if (axios.isAxiosError(e)) {
        throw new Error(`HTTP error! status: ${e.response?.status} - ${e.message}`);
      }
      throw e;
    }
  },
};

export default cutTubeService;

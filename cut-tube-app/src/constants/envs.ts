import type { Envs } from "@/types/envs";

const envs: Envs = {
  apiUrl: import.meta.env.VITE_API_URL as string,
};

export default envs;

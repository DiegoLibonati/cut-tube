import type { Clip } from "@/types/app";

export type FormClip = Pick<Clip, "filename" | "end" | "start" | "url">;

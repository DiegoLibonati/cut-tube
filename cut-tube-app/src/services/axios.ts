import axios from "axios";

export const apiCutTube = axios.create({
  baseURL: "/api/v1/cut",
  headers: {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
  },
});

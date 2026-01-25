import axios from "axios";

const API = axios.create({ baseURL: "http://127.0.0.1:8000" });

export const uploadDataset = (file) => {
  const fd = new FormData();
  fd.append("file", file);
  return API.post("/upload", fd);
};

export const fetchData = () => API.get("/data");
export const predict = (p) => API.post("/predict", p);

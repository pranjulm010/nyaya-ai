import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api";

export const uploadPDF = async (file: File) => {

  const formData = new FormData();

  formData.append("file", file);

  const response = await axios.post(
    `${BASE_URL}/upload/`,
    formData
  );

  return response.data;
};

export const sendMessage = async (query: string) => {

  const response = await axios.post(
    `${BASE_URL}/chat/`,
    {
      query,
    }
  );

  return response.data;
};
import axios from "axios";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const uploadDocument = async (
  file: File,
  userId: string = "anonymous"
) => {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("user_id", userId);

  const response = await axios.post(
    `${BASE_URL}/upload-document/`,
    formData
  );

  return response.data;
};

// old name support
export const uploadPDF = uploadDocument;

export const sendMessage = async ({
  query,
  userId = "anonymous",
  sessionId,
  userType = "public",
  documentId,
  documentType,
}: {
  query: string;
  userId?: string;
  sessionId?: string;
  userType?: "public" | "lawyer";
  documentId?: string;
  documentType?: string;
}) => {
  const response = await api.post("/chat/", {
    query,
    user_id: userId,
    session_id: sessionId,
    user_type: userType,
    document_id: documentId,
    document_type: documentType,
  });

  return response.data;
};

export const getHistory = async (
  userId: string,
  sessionId: string
) => {
  const response = await api.get("/history/", {
    params: {
      user_id: userId,
      session_id: sessionId,
    },
  });

  return response.data;
};

export const getUsage = async (userId: string) => {
  const response = await api.get("/usage/", {
    params: {
      user_id: userId,
    },
  });

  return response.data;
};

export const checkBackendHealth = async () => {
  const response = await api.get("/health/");
  return response.data;
};
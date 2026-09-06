export interface MessageProps {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp?: string;
}

export interface Step {
  id: string;
  label: string;
  status: "pending" | "running" | "completed" | "error";
  duration?: string;
}

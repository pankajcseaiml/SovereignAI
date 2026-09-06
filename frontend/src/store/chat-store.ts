import { create } from 'zustand';
import { MessageProps, Step } from '../types/chat';

interface ChatState {
  messages: MessageProps[];
  agentSteps: Step[];
  isRunning: boolean;
  socket: WebSocket | null;
  addMessage: (msg: MessageProps) => void;
  updateStep: (stepId: string, status: Step['status']) => void;
  connectSocket: (conversationId: string) => void;
  sendMessage: (content: string) => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  agentSteps: [
    { id: '1', label: 'Initialize workspace', status: 'completed' },
    { id: '2', label: 'Load context', status: 'completed' }
  ],
  isRunning: false,
  socket: null,

  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),

  updateStep: (stepId, status) => set((state) => ({
    agentSteps: state.agentSteps.map(step => 
      step.id === stepId ? { ...step, status } : step
    ),
    isRunning: status === 'running' || state.agentSteps.some(s => s.id !== stepId && s.status === 'running')
  })),

  connectSocket: (conversationId: string) => {
    // Prevent duplicate connections
    if (get().socket) return;

    const wsUrl = `ws://localhost:8001/api/v1/chats/ws/${conversationId}`;
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      console.log(`Connected to WS: ${wsUrl}`);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'message') {
          get().addMessage({
            id: Date.now().toString(),
            role: data.role,
            content: data.content,
          });
        } else if (data.type === 'agent_progress') {
          // Add or update the step
          set((state) => {
            const existing = state.agentSteps.find(s => s.label === data.step);
            if (existing) {
              return {
                agentSteps: state.agentSteps.map(s => 
                  s.label === data.step ? { ...s, status: data.status } : s
                ),
                isRunning: data.status === 'running'
              };
            } else {
              return {
                agentSteps: [...state.agentSteps, {
                  id: Date.now().toString(),
                  label: data.step,
                  status: data.status
                }],
                isRunning: data.status === 'running'
              };
            }
          });
        }
      } catch (err) {
        console.error("Failed to parse WS message", err);
      }
    };

    socket.onclose = () => {
      console.log("WS closed");
      set({ socket: null });
    };

    set({ socket });
  },

  sendMessage: (content: string) => {
    const { socket, addMessage } = get();
    // Optimistic UI update
    addMessage({
      id: Date.now().toString(),
      role: 'user',
      content: content
    });

    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(content);
    } else {
      console.warn("WebSocket not connected");
    }
  }
}));

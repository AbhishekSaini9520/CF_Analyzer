import { useState, useRef, useEffect } from "react";
import { Send, Bot, User } from "lucide-react";
import { API_BASE } from "../api";

export default function AIChat() {
  const [messages, setMessages] = useState([
    { role: "ai", content: "Ask me anything about your performance." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { role: "ai", content: data.answer || "I'm sorry, I couldn't process that." },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: "⚠️ Server error. Please check your connection." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex justify-center mt-6">
      <div className="w-[80vw] bg-white rounded-xl shadow border p-6 max-w-7xl space-y-6">

        {/* Header */}
        <header className="px-8 py-5 border-b bg-white flex items-center gap-3">
          <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
            <Bot size={24} />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-800 tracking-tight">Gen AI Assistant</h2>
            <p className="text-xs text-gray-400 font-medium uppercase tracking-wider">
              Codeforces Performance Insights
            </p>
          </div>
        </header>

        {/* Chat Message Feed */}
        <main className="flex-1 overflow-y-auto px-6 py-6 space-y-6 bg-gray-50/50">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex items-end gap-2 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"
                }`}
            >
              {/* Avatar Icons */}
              <div className={`flex-shrink-0 p-2 rounded-full ${msg.role === "user" ? "bg-blue-600 text-white" : "bg-gray-300 text-gray-600"
                }`}>
                {msg.role === "user" ? <User size={14} /> : <Bot size={14} />}
              </div>

              {/* Message Bubble */}
              <div
                className={`px-4 py-3 rounded-2xl max-w-[75%] text-sm leading-relaxed shadow-sm ${msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-white text-gray-800 border border-gray-200 rounded-bl-none"
                  }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {loading && (
            <div className="flex items-center gap-2 text-gray-400 italic text-xs ml-10">
              <span className="flex gap-1">
                <span className="animate-bounce">.</span>
                <span className="animate-bounce [animation-delay:0.2s]">.</span>
                <span className="animate-bounce [animation-delay:0.4s]">.</span>
              </span>
              AI is analyzing your stats
            </div>
          )}
          <div ref={bottomRef} />
        </main>

        {/* Input Footer */}
        <footer className="p-6 bg-white border-t">
          <div className="flex items-center gap-3 bg-gray-100 rounded-2xl px-4 py-3 focus-within:ring-2 focus-within:ring-blue-500 transition-all">
            <input
              type="text"
              placeholder="Ask about your rating, contests, or problems..."
              className="flex-1 bg-transparent outline-none text-gray-700 placeholder:text-gray-400"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />

            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="p-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors shadow-md shadow-blue-200"
              aria-label="Send message"
            >
              <Send size={20} />
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
}
"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send, Plane, MapPin, Loader2, Sparkles } from "lucide-react";

type Message = {
  id: string;
  role: "user" | "agent";
  content: string;
  tools_called?: string[];
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init",
      role: "agent",
      content: "Chào bạn! Mình là TravelBuddy, sẵn sàng giúp bạn lên kế hoạch chuyến đi tuyệt vời tại Việt Nam nha. Bạn muốn đi đâu mùa hè này?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => Math.random().toString(36).substring(2, 15));
  const [tripSummary, setTripSummary] = useState({
    flights: "",
    hotels: "",
    total_cost: "0đ"
  });
  
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { id: Date.now().toString(), role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: userMessage.content, session_id: sessionId }),
      });
      
      const data = await res.json();
      
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "agent",
        content: data.final_response || "Oops! Có lỗi một xíu, bạn thử lại nhé.",
        tools_called: data.tools_called,
      };
      
      setMessages((prev) => [...prev, agentMessage]);

      if (data.trip_summary) {
        setTripSummary(data.trip_summary);
      }
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { id: Date.now().toString(), role: "agent", content: "Xin lỗi, hiện tại không thể kết nối tới server. 😢" }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex h-screen p-4 md:p-8 gap-6 max-w-7xl mx-auto w-full">
      
      {/* 70% Chat Area */}
      <section className="flex-[7] flex flex-col bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden border border-orange-100">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-orange-400 to-amber-400 p-6 flex items-center gap-3 text-white">
          <div className="bg-white/20 p-2 rounded-2xl backdrop-blur-sm">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold">TravelBuddy</h1>
            <p className="text-sm font-medium text-white/80">Your Artistic Travel Agent</p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex flex-col $ {msg.role === "user" ? "items-end" : "items-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-5 py-3.5 ${
                  msg.role === "user"
                    ? "bg-slate-900 text-white rounded-tr-sm"
                    : "bg-slate-50 text-slate-800 border border-slate-100 rounded-tl-sm shadow-sm"
                }`}
              >
                <div className="whitespace-pre-wrap leading-relaxed">{msg.content}</div>
              </div>
              
              {/* Tool Execution Logs */}
              {msg.tools_called && msg.tools_called.length > 0 && (
                <div className="mt-2 flex gap-2 ml-2">
                  {msg.tools_called.map((tool) => (
                    <span key={tool} className="text-[10px] uppercase font-bold tracking-wider px-2 py-1 bg-orange-100 text-orange-600 rounded-full">
                      Used: {tool}
                  </span>
                  ))}
                </div>
              )}
            </motion.div>
          ))}
          
          {isLoading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-start">
              <div className="bg-slate-50 border border-slate-100 rounded-2xl rounded-tl-sm px-6 py-4 shadow-sm flex items-center gap-2 text-slate-500">
                <Loader2 className="w-4 h-4 animate-spin text-orange-500" />
                <span className="text-sm font-medium">Đang tìm mòn mỏi...</span>
              </div>
            </motion.div>
          )}
          <div ref={endOfMessagesRef} />
        </div>

        {/* Input Form */}
        <div className="p-4 bg-white border-t border-slate-50">
          <form onSubmit={handleSubmit} className="flex gap-3 bg-slate-50 p-2 rounded-2xl border border-slate-100 focus-within:ring-2 focus-within:ring-orange-200 transition-all">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ví dụ: Tìm vé máy bay từ Hà Nội đi Đà Nẵng, budget 5 triệu..."
              className="flex-1 bg-transparent px-4 py-2 outline-none text-slate-700 placeholder:text-slate-400"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white p-3 rounded-xl transition-colors shadow-sm cursor-pointer disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>
      </section>

      {/* 30% Trip Summary Sidebar */}
      <aside className="flex-[3] hidden lg:flex flex-col gap-4">
        <div className="bg-white p-6 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-orange-100 flex-1">
          <div className="flex items-center gap-2 mb-6 text-slate-800">
            <MapPin className="w-5 h-5 text-orange-500" />
            <h2 className="text-xl font-bold">Trip Summary</h2>
          </div>
          
          <div className="space-y-6">
            <div className="p-4 rounded-2xl bg-gradient-to-br from-orange-50/50 to-amber-50/50 border border-orange-100/50">
              <div className="flex items-center gap-2 mb-2 text-orange-700 font-semibold">
                <Plane className="w-4 h-4" /> <h3>Chuyến Bay</h3>
              </div>
              <p className={`text-sm leading-relaxed ${tripSummary.flights ? 'text-slate-800 font-medium' : 'text-slate-500 italic'}`}>
                {tripSummary.flights || "Chưa có chuyến bay nào được chọn. Hãy chat với TravelBuddy nhé!"}
              </p>
            </div>
            
            <div className="p-4 rounded-2xl bg-gradient-to-br from-cyan-50/50 to-emerald-50/50 border border-cyan-100/50">
              <div className="flex items-center gap-2 mb-2 text-cyan-700 font-semibold">
                <span className="text-lg">🏨</span> <h3>Khách Sạn</h3>
              </div>
              <p className={`text-sm leading-relaxed ${tripSummary.hotels ? 'text-slate-800 font-medium' : 'text-slate-500 italic'}`}>
                {tripSummary.hotels || "Chưa có khách sạn nào được chọn."}
              </p>
            </div>
            
            <div className="pt-4 border-t border-slate-100">
              <div className="flex justify-between items-center bg-slate-900 text-white p-4 rounded-2xl shadow-md">
                <span className="font-medium text-slate-300">Tổng chi phí</span>
                <span className="text-xl font-bold">{tripSummary.total_cost || "0đ"}</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Aesthetic filler */}
        <div className="h-32 rounded-3xl bg-gradient-to-tr from-amber-200 to-orange-400 opacity-90 p-6 flex flex-col justify-end overflow-hidden relative shadow-sm">
          <div className="absolute top-[-20%] right-[-10%] w-32 h-32 bg-white/20 rounded-full blur-2xl"></div>
          <h3 className="text-white font-bold text-lg z-10 leading-tight">Summer Vibes<br/>Edition</h3>
        </div>
      </aside>
    </main>
  );
}

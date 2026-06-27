import { useState, useRef } from "react";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import UploadPDF from "../components/UploadPDF";
import WebsiteLoader from "../components/WebsiteLoader";
import ChatWidget from "../components/ChatWidget";
import ChatInput from "../components/ChatInput";
import HistoryPanel from "../components/HistoryPanel";
import Footer from "../components/Footer";

function Home() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  // Section refs
  const uploadRef = useRef(null);
  const websiteRef = useRef(null);
  const chatRef = useRef(null);

  const scrollToSection = (section) => {
    if (section === "upload") {
      uploadRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }

    if (section === "website") {
      websiteRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }

    if (section === "chat") {
      chatRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  return (
    <div className="h-screen bg-gray-100 flex">

      <Sidebar
        setShowHistory={setShowHistory}
        scrollToSection={scrollToSection}
      />

      <div className="flex-1 flex flex-col overflow-hidden">

        <Header />

        <main className="flex-1 overflow-y-auto p-6">

          {/* Upload + Website */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

            <div ref={uploadRef}>
              <UploadPDF />
            </div>

            <div ref={websiteRef}>
              <WebsiteLoader />
            </div>

          </div>

          {/* Chat */}
          <div
            ref={chatRef}
            className="flex flex-col h-[calc(100vh-340px)]"
          >

            <ChatWidget
              messages={messages}
              loading={loading}
            />

            <ChatInput
              messages={messages}
              setMessages={setMessages}
              setLoading={setLoading}
            />

          </div>

        </main>

        <Footer />

      </div>

      {showHistory && (
        <HistoryPanel
          setShowHistory={setShowHistory}
        />
      )}

    </div>
  );
}

export default Home;
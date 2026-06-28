import { useState } from "react";

import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import About from "../components/About";
import Menu from "../components/Menu";
import Gallery from "../components/Gallery";
import Contact from "../components/Contact";
import Footer from "../components/Footer";

import FloatingChatButton from "../components/FloatingChatButton";
import CustomerChat from "../components/CustomerChat";

function Home() {
  const [chatOpen, setChatOpen] = useState(false);

  return (
    <div className="bg-gray-50 min-h-screen">

      <Navbar
        onOpenChat={() => setChatOpen(true)}
      />

      <Hero
        onOpenChat={() => setChatOpen(true)}
      />

      <About />

      <Menu />

      <Gallery />

      <Contact />

      <Footer />

      <FloatingChatButton
        onClick={() => setChatOpen(true)}
      />

      <CustomerChat
        open={chatOpen}
        onClose={() => setChatOpen(false)}
      />

    </div>
  );
}

export default Home;
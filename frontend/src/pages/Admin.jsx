import { useState } from "react";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import UploadPDF from "../components/UploadPDF";
import WebsiteLoader from "../components/WebsiteLoader";
import HistoryPanel from "../components/HistoryPanel";

function Admin() {
  const [showHistory, setShowHistory] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100 flex">

      {/* Sidebar */}

      <Sidebar
        setShowHistory={setShowHistory}
        scrollToSection={() => {}}
      />

      {/* Main */}

      <div className="flex-1 flex flex-col">

        <Header />

        <main className="flex-1 p-8 overflow-y-auto">

          <div className="mb-8">

            <h1 className="text-3xl font-bold text-gray-800">
              Admin Dashboard
            </h1>

            <p className="text-gray-500 mt-2">
              Manage your Restaurant AI Knowledge Base.
            </p>

          </div>

          <div className="grid lg:grid-cols-2 gap-8">

            <UploadPDF />

            <WebsiteLoader />

          </div>

        </main>

      </div>

      {showHistory && (
        <HistoryPanel
          setShowHistory={setShowHistory}
        />
      )}

    </div>
  );
}

export default Admin;
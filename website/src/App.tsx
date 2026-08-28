import { BrowserRouter, Route, Routes } from "react-router-dom";
import ContextList from "./pages/ContextList";
import ParticipantList from "./pages/ParticipantList";
import ConversationView from "./pages/ConversationView";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ContextList />} />
        <Route path="/context/:contextId" element={<ParticipantList />} />
        <Route path="/context/:contextId/participant/:participantId" element={<ConversationView />} />
      </Routes>
    </BrowserRouter>
  );
}

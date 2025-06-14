import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import VoiceTextAssistant from './VoiceTextAssistant'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './home.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* use browser router */}
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chatbot" element={<VoiceTextAssistant />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)

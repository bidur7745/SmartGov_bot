import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import First from './First.jsx'
import Second from './Second.jsx'
import Formsubmit from './Formsubmit.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<First />} />
        <Route path="/second" element={<Second />} />
        <Route path="/formsubmit" element={<Formsubmit />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)

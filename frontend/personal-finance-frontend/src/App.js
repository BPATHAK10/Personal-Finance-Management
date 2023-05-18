import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignIn from './pages/Login/Login';
import Dashboard from "./pages/Dashboard/Dashboard"

function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Routes>
        <Route  exact path="/" element={<SignIn />} />
        <Route  path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
   </div>
  );
}

export default App;

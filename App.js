import React from "react";
import "./App.css";

import CodeEditor from "./Components/CodeEditor";
import logo from "./assets/logo.png";
import Profile from "./Components/Profile";

function App() {
  return (
    <div className='App'>
      <img src={logo} alt='' />
      <CodeEditor />
      <div className='profile-section'>
        <Profile />
      </div>
    </div>
  );
}

export default App;

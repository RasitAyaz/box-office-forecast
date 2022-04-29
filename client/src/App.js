import './App.css';
import { Route, Routes, useNavigate } from "react-router-dom";
import Home from './pages/Home';
import { useEffect, useState } from 'react';
import MoviePage from './pages/MoviePage';

function App() {
  const history = useNavigate();

  return (
    <div className="App">
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/movie/:id" element={<MoviePage />} />
        <Route path="*" status={404} element={"404"} />
      </Routes>
    </div>
  );
}

export default App;

import './App.css';
import { Route, Routes, useNavigate } from "react-router-dom";
import Home from './components/pages/Home';

function App() {
  const history = useNavigate();

  const onClickLogo = () => {
    history("/");
  };

  const onClickCustom = () => {
    history("/custom");
  };

  return (
    <div className="App">
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/custom" element={"custom"} />
      </Routes>
    </div>
  );
}

export default App;

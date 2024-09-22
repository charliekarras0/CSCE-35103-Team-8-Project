import React, { useState, useEffect } from 'react';
import axios from 'axios';
import logo from './logo.jpg';
import './App.css'; // Ensure you have appropriate styling

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [playerData, setPlayerData] = useState({ id: '', codename: ''});
  const [errors, setErrors] = useState({});

  useEffect(() => {
    const timer = setTimeout(() => setShowSplash(false), 5000);
    return () => clearTimeout(timer);
  }, []);

  const validate = () => {
    const errors = {};
    if (!playerData.id) {
      errors.id = 'Player ID is required';
    } else if (!Number.isInteger(Number(playerData.id))) {
      errors.id = 'Player ID must be an integer';
    }

    if (!playerData.codename) {
      errors.codename = 'Codename is required';
    }

    

    setErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (e) => {
    setPlayerData({ ...playerData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) {
      return;
    }
    try {
      await axios.post('http://localhost:3000/add_player', playerData);
      alert('Player added successfully');
      setPlayerData({ id: '', codename: ''});
      setErrors({});
    } catch (error) {
      console.error('Error adding player:', error);
      if (error.response) {
		  alert(error.response);
		  alert("server responsed");
	  }
	  else if (error.request) {
		  alert(error.request);
		  alert(`Request Error: ${JSON.stringify(error.request)}`);
		  alert("network error");
	  } else {
		  alert("We in deep trouble");
	  }
      if (error.response && error.response.data && error.response.data.error) {
        alert(`Error: ${error.response.data.error}`);
      } else {
        alert('An unexpected error occurred while adding the player.');
      }
    }
  };

  if (showSplash) {
    return (
      <div className="splash-screen" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: 'black' }}>
        <img src={logo} alt="Game Logo" style={{ maxWidth: '100%', maxHeight: '100%' }} />
      </div>
    );
  }

  return (
    <div className="player-entry">
      <h1>Player Entry</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="id">Player ID:</label>
          <input
            type="text"
            name="id"
            id="id"
            value={playerData.id}
            onChange={handleInputChange}
            placeholder="Player ID"
            required
          />
          {errors.id && <span className="error">{errors.id}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="codename">Codename:</label>
          <input
            type="text"
            name="codename"
            id="codename"
            value={playerData.codename}
            onChange={handleInputChange}
            placeholder="Codename"
            required
          />
          {errors.codename && <span className="error">{errors.codename}</span>}
        </div>

        

        <button type="submit">Add Player</button>
      </form>
    </div>
  );
}

export default App;

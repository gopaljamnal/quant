import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState('');
  useEffect(() => {
    const fetchMessage =  async () => {
      try{
        const response = await axios.get('http://127.0.0.1:5000/api/greet');
        setMessage(response.data.message);
        console.log(message)
      } catch (error) {
        console.error('Error fetching message:', error)
      }
    };
    fetchMessage();

  }, []);
  return (
    <div className="App">
      <h1> {message ? message : "Loading..."}</h1>
    </div>
  );
}

export default App;

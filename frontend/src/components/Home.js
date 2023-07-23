import React from 'react'
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import {render} from "react-dom";
import Room from "./Room";
import CreateRoom from "./CreateRoom";
import JoinRoom from "./JoinRoom";

function Home() {
  return (
    <Router>
        <Routes>
            <Route exact path='/' element={<Home/>} />
            <Route path='/create-room' element={<CreateRoom/>} />
            <Route path='/join-room' element={<JoinRoom/>} />
            <Route path='/room/:code' element={<Room/>} />
        </Routes>      
         
    </Router>
  )
}

export default Home

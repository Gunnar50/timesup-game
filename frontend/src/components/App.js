import React from "react";
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import {render} from "react-dom";
import Room from "./Room";
import CreateRoom from "./CreateRoom";
import JoinRoom from "./JoinRoom";
import Home from "./Home";

export default function App(){
    return (
        <Router>
            <Routes>
                <Route exact path='/' element={<Home/>} />
                <Route path='/create-room' element={<CreateRoom/>} />
                <Route path='/join-room' element={<JoinRoom/>} />
            </Routes>      
         
        </Router>
    );
}

const appDiv = document.getElementById("app");
render(<App/>, appDiv);

import React from 'react'
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Room from "./Room";
import CreateRoom from "./CreateRoom";
import JoinRoom from "./JoinRoom";
import { useNavigate } from 'react-router-dom';

function HomePage() {
	const navigate = useNavigate();
	return (
		<div>
			<h1>Times Up!</h1>
			<button onClick={() => {navigate("/create-room")}}>Create a Room</button>
			<button onClick={() => {navigate("/join-room")}}>Join a Room</button>
			<button onClick={() => {navigate("/join-room")}}>How to</button>
		</div>
	);
}

function Home() {
	

	return (
		<Router>
			<Routes>
				<Route exact path='/' element={<HomePage/>} />
				<Route path='/create-room' element={<CreateRoom/>} />
				<Route path='/join-room' element={<JoinRoom/>} />
				<Route path='/room/:code' element={<Room/>} />
			</Routes>      
			
		</Router>
	)
}

export default Home

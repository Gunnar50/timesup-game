import React, { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Room from "./Room";
import CreateRoom from "./CreateRoom";
import JoinRoom from "./JoinRoom";
import { useNavigate, Navigate } from 'react-router-dom';

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
	
	const [code, setCode] = useState(null);

	const getUserInRoom = () => {
		fetch("/api/user-in-room")
		.then(res => res.json())
		.then(data => setCode(data.code));
	}

	useEffect(() => getUserInRoom(), []);

	const clearRoomCode = () => {
		setCode(null);
	}


	return (
		<Router>
			<Routes>
				<Route exact path='/' element={code ? <Navigate to={`/room/${code}`} /> : <HomePage/>} />
				<Route path='/create-room' element={<CreateRoom/>} />
				<Route path='/join-room' element={<JoinRoom/>} />
				<Route path='/room/:code' element={<Room leaveRoomCallBack={clearRoomCode} />} />
			</Routes>      
		</Router>
	)
}

export default Home

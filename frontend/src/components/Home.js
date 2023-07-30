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
	// const socket = new WebSocket(`ws://localhost:8000/ws/game/`);
	// const socket = new WebSocket(`ws://127.0.0.1:8000/ws/game/`);

	// socket.onopen = () => {
	// 	console.log("WebSocket connection opened");
	// };
	
	// socket.onerror = (error) => {
	// 	console.log("WebSocket error: ", error);
	// };
	
	// socket.onclose = (event) => {
	// 	console.log("WebSocket connection closed: ", event);
	// };
	
	
	// useEffect(() => {
	// 	socket.onmessage = (e) => {
	// 		let data = JSON.parse(e.data);
	// 		console.log(data.value);
	// 	};

	// 	return () => {
	// 		socket.close();
	// 	}
	// }, []);

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

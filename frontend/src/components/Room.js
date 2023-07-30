import React, { useEffect, useState, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';
import getCsrfToken from "./GetCSRF";

function Room(props) {
	const intervalRef = useRef();
	const socketRef = useRef();
	const navigate = useNavigate();
	const {code} = useParams();
	const [details, setDetails] = useState(null);
	const [users, setUsers] = useState([]);

	const getRoomDetails = () => {
		fetch(`/api/get-room?code=${code}`)
		.then((res) => {
			if(!res.ok) {
				props.leaveRoomCallBack();
				navigate("/join-room");
			} else return res.json();
		})
		.then(data => setDetails(data));
	};

	const handleExitRoomButton = () => {
		getCsrfToken().then(csrfToken => {
			fetch("/api/exit-room", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					'X-CSRFToken': csrfToken,
				},
			}).then((res) => {
				props.leaveRoomCallBack();
				navigate("/");
			})
		})
		
	}

	const getUsers = () => {
		fetch(`/api/get-users?code=${code}`)
		.then(res => res.json())
		.then(data => setUsers(data));
	};

	useEffect(() => {getRoomDetails();getUsers();}, []);

	// useEffect(() => {
    //     intervalRef.current = setInterval(getUsers, 1000);
    //     return () => {
    //         clearInterval(intervalRef.current);
    //     }
    // }, []);

	useEffect(() => {
		socketRef.current = new WebSocket(`ws://localhost:8000/ws/game${window.location.pathname}/`);
	
		socketRef.current.onmessage = function(event) {
			const data = JSON.parse(event.data);
			const command = data.command;
			console.log(command);  // Do something with this message

			if(command === "message") {
				console.log(data.message);
				console.log("Starting...");
			}
			if(command === "joined") { 
				let user = data.user;
				console.log(user);
			}
		}
	
		// Make sure to close the WebSocket connection when the component unmounts
		return () => {
			socketRef.current.close();
		}
	}, []);

	useEffect(() => {
		socketRef.current.onopen = () => {
			socketRef.current.send(
				JSON.stringify({
					command: "joined",
					user: users,
				})
			);
		};
	}, []);

	const handleStartGameButton = () => {
		const message = JSON.stringify({command: "message", message: "StartGame"});
		socketRef.current.send(message);
	}


	if(!details) return null;

	return (
		<div>
			<h2>Room Code: {code}</h2>
			{details.is_host && <button onClick={() => {handleStartGameButton()}}>Start</button>}
			<button onClick={() => {handleExitRoomButton()}}>Exit</button>

			<p>When the game starts you have to write {details.words_per_user} words.</p>

			<h4>Users in the room:</h4>
			<ul>
				{users.map((user, index) => (
					<li key={index}>{user.username}</li>
				))}
			</ul>

		</div>
	)
}

export default Room

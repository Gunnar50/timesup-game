import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

function Room() {
	const code = useParams()["code"];
	const [details, setDetails] = useState(null);
	const [users, setUsers] = useState([]);

	const getRoomDetails = () => {
		fetch(`/api/get-room?code=${code}`)
		.then(res => res.json())
		.then(data => setDetails(data));
	};

	const getUsers = () => {
		fetch(`/api/get-users?code=${code}`)
		.then(res => res.json())
		.then(data => setUsers(data));
	};

	useEffect(() => (
		getRoomDetails(),
		getUsers()
	), []);

	return (
		<div>
			<h2>Room Code: {code}</h2>


			<h4>Users in the room:</h4>
			<ul>
				{users.map((user) => (
					<li>{user.username}</li>
				))}
			</ul>

		</div>
	)
}

export default Room

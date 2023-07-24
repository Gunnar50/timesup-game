import React, { useEffect, useState, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';

function Room(props) {
	const intervalRef = useRef();
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

	const getUsers = () => {
		fetch(`/api/get-users?code=${code}`)
		.then(res => res.json())
		.then(data => setUsers(data));
	};

	useEffect(() => getRoomDetails(), []);

	useEffect(() => {
        intervalRef.current = setInterval(getUsers, 1000);
        return () => {
            clearInterval(intervalRef.current);
        }
    }, []);


	if(!details) return null;

	return (
		<div>
			<h2>Room Code: {code}</h2>
			{details.is_host && <button>Start</button>}

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

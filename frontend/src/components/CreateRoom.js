import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import getCsrfToken from "./GetCSRF";
// import 'bootstrap/dist/css/bootstrap.css';


function CreateRoom() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [words_per_user, setWordsPerUser] = useState(3);
    const [num_teams, setNumTeams] = useState(2);

    const handleSubmit = (e) => {
        e.preventDefault();
        
        getCsrfToken().then(csrfToken => {
            fetch("/api/create-room", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        "username": username,
                        "words_per_user": words_per_user,
                        "num_teams": num_teams
                    }),  
            })
            .then((res) => {
            if (!res.ok) throw new Error(res.status);
            return res.json();
        })
        .then((data) => {
            console.log(data);
            navigate("/");
        }).catch(err => console.log(err));
        });
        
        
    }

    return (
        <div>
            <h1>Create Room</h1>
            <div>
                <form onSubmit={handleSubmit}>
                    <label>Username</label>
                    <input type="text" onChange={(e) => {setUsername(e.target.value)}}/>
                    <label>Words Per Player</label>
                    <input type="number" value={words_per_user} onChange={(e) => {setWordsPerUser(e.target.value)}}/>
                    <label>Number of Teams</label>
                    <input type="number" value={num_teams} onChange={(e) => {setNumTeams(e.target.value)}}/>
                    <button type="submit" className="btn btn-primary">Create Room</button>
                </form>
            </div>
        </div>
    )
}

export default CreateRoom

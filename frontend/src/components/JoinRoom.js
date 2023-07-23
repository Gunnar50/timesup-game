import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import getCsrfToken from "./GetCSRF";


function JoinRoom() {
	const [code, setCode] = useState("");
	const [username, setUsername] = useState("");

	const handleSubmit = (e) => {
		e.preventDefault();
        
        getCsrfToken().then(csrfToken => {
            fetch("/api/join-room", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        "username": username,
                        "code": code,
                    }),  
            })
            .then((res) => {
            if (!res.ok) throw new Error(res.status);
            return res.json();
        })
        .then((data) => {
            console.log(data);
            // navigate("/");
        }).catch(err => console.log(err));
        });
	};

    return (
      <div>
          <h1>Join A Room</h1>
          <div>
              <form onSubmit={handleSubmit}>
                  <label>Room Code</label>
				  <br/>
                  <input type="text" value={code} onChange={(e) => {setCode(e.target.value)}}/>
                  <br/>
				  <label>Username</label>
				  <br/>
                  <input type="text"value={username} onChange={(e) => {setUsername(e.target.value)}}/>
                  <br/>
				  <button type="submit" className="btn btn-primary">Join A Room</button>
              </form>
          </div>
      </div>
    )
}

export default JoinRoom

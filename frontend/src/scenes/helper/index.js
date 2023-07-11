import React, { useState } from "react";
import { Container, TextField, Button } from "@mui/material";
import Navbar from "../navbar";

function Helper() {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handleMessageChange = (event) => {
        setMessage(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        // Code to send the email
        // You can use an API or server-side implementation to send the email
    };

    return (
        <div>
            <Navbar />
            <Container
                maxWidth="sm"
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    marginTop: "2rem",
                }}
            >
                <form onSubmit={handleSubmit} sx={{ width: "100%" }}>
                    <TextField
                        label="Email"
                        type="email"
                        value={email}
                        onChange={handleEmailChange}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        label="Message"
                        value={message}
                        onChange={handleMessageChange}
                        multiline
                        rows={4}
                        fullWidth
                        margin="normal"
                    />
                    <Button variant="contained" type="submit">
                        Send Email
                    </Button>
                </form>
            </Container>
        </div>
    );
}

export default Helper;

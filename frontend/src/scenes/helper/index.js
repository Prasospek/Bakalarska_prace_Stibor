import React, { useState } from "react";
import { Container, TextField, Button, Typography } from "@mui/material";
import Navbar from "../navbar";

function Helper() {
    const [userEmail, setUserEmail] = useState("");
    const [message, setMessage] = useState("");

    const handleEmailChange = (event) => {
        setUserEmail(event.target.value);
    };

    const handleMessageChange = (event) => {
        setMessage(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        fetch("http://localhost:8001/api/submit-email/", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({ email: userEmail, message }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                // TODO: Handle success
                setUserEmail(""); // Reset userEmail state to an empty string
                setMessage(""); // Reset message state to an empty string
            })
            .catch((error) => {
                console.log(error);
                // TODO: Handle error
            });
    };

    return (
        <div>
            <Navbar />
            <Typography
                variant="h4" // Change the variant to h2 for a bigger font size
                align="center" // Keep the alignment centered
                sx={{
                    marginTop: "4rem", // Increase the marginTop value for more spacing
                    fontWeight: 700, // Add font weight for emphasis
                    fontStyle: "italic", // Add italic style
                }}
            >
                Máte problém s ShareTaxMax nebo máte jen otázku ? Neváhejte nám
                napsat
            </Typography>

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
                        value={userEmail}
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
                    <Button
                        variant="contained"
                        type="submit"
                        sx={{
                            marginTop: "1rem",
                        }}
                    >
                        Send Email
                    </Button>
                </form>
            </Container>
        </div>
    );
}

export default Helper;

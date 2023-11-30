import React, { useState } from "react";
import { Container, TextField, Button, Typography } from "@mui/material";
import Navbar from "../navbar";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function Helper() {
    const [userEmail, setUserEmail] = useState("");
    const [message, setMessage] = useState("");

    const handleEmailChange = (event) => {
        setUserEmail(event.target.value);
    };

    const handleMessageChange = (event) => {
        setMessage(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch(
                `${process.env.REACT_APP_BACKEND}/api/submit-email/`,

                {
                    method: "POST",
                    headers: {
                        "Content-type": "application/json",
                    },
                    body: JSON.stringify({ email: userEmail, message }),
                }
            );

            if (response.ok) {
                const data = await response.json();
                console.log(data);

                setUserEmail(""); // Reset userEmail state to an empty string
                setMessage(""); // Reset message state to an empty string
                toast.success(`Email byl úspěšně odeslán !`);
            } else {
                throw new Error(
                    "Request failed with status: " + response.status
                );
            }
        } catch (error) {
            console.log(error);
            toast.error("Stala se chyba! Email nebyl odeslán.");
        }
    };

    return (
        <div>
            <Navbar />
            <Typography
                variant="h4"
                align="center"
                sx={{
                    marginTop: "12rem",
                    fontWeight: 700,
                    fontStyle: "italic",
                }}
            >
                Máte technický problém nebo otázku ? Neváhejte nám napsat
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
            <ToastContainer />
        </div>
    );
}

export default Helper;

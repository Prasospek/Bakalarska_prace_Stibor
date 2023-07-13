import React from "react";
import Navbar from "../navbar";
import { Box, Typography, Button, Card, CardMedia } from "@mui/material";
import { useNavigate } from "react-router-dom";
import pic from "../../assets/pic.jpg";

const MainPage = () => {
    const navigate = useNavigate();

    const handleNavigate = () => {
        navigate("/konverter");
    };

    return (
        <div>
            <Navbar />

            <Box marginTop={"4rem"} marginLeft={"6rem"}>
                <Box width={"40%"}>
                    <Box>
                        <Typography variant="h1">
                            Grow your business with Facebook and Instagram -
                            From one place
                        </Typography>
                    </Box>
                    <Box marginTop={"2rem"}>
                        <Typography variant="h4">
                            Lorem ipsum dolor sit amet consectetur adipisicing
                            elit. Fugit placeat est, assumenda tenetur rerum
                            dolorem
                        </Typography>
                    </Box>
                    <Box>
                        <Button
                            className="button-36"
                            sx={{
                                fontSize: "0.9rem",
                                marginTop: "2rem",
                            }}
                            onClick={handleNavigate}
                        >
                            Kovertovat CSV
                        </Button>
                    </Box>
                </Box>

                <Box marginTop={"10rem"} width={"50%"} display={"flex"}>
                    <Box width={"25%"} marginRight={"5rem"}>
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Hello
                        </Typography>
                        <Typography variant="h4">
                            Lorem ipsum dolor sit amet consectetur adipisicing
                            elit. Fugit placeat est, assumenda tenetur rerum
                            dolorem 1111
                        </Typography>
                    </Box>
                    <Box width={"25%"} marginRight={"5rem"}>
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Hello
                        </Typography>
                        <Typography variant="h4">
                            Lorem ipsum dolor sit amet consectetur adipisicing
                            elit. Fugit placeat est, assumenda tenetur rerum
                            dolorem 2222
                        </Typography>
                    </Box>
                    <Box width={"25%"} marginRight={"5rem"}>
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Hello
                        </Typography>
                        <Typography variant="h4">
                            Lorem ipsum dolor sit amet consectetur adipisicing
                            elit. Fugit placeat est, assumenda tenetur rerum
                            dolorem 3333
                        </Typography>
                    </Box>
                </Box>
            </Box>
        </div>
    );
};

export default MainPage;

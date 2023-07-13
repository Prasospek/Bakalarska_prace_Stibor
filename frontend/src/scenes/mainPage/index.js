import React from "react";
import Navbar from "../navbar";
import { Box, Typography, Button, Card, CardMedia } from "@mui/material";
import { useNavigate } from "react-router-dom";
import pic from "../../assets/trader.jpg";

const MainPage = () => {
    const navigate = useNavigate();

    const handleNavigate = () => {
        navigate("/konverter");
    };

    return (
        <div style={{ width: "100%", height: "100%", overflow: "hidden" }}>
            <Navbar />

            <Box
                marginTop={"4rem"}
                marginLeft={"6rem"}
                position="relative"
                style={{ height: "calc(100% - 4rem)", overflowY: "hidden" }}
            >
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

                <Box
                    marginTop={"10rem"}
                    width={"50%"}
                    display={"flex"}
                    style={{ height: "calc(100% - 10rem)" }}
                >
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
            <Box
                position="absolute"
                top="6rem"
                left="60rem"
                transform="translateY(-50%)"
                height={"100%"}
                width={"100%"}
                z-zIndex={"-1"}
            >
                <Card
                    sx={{
                        maxWidth: "70%",
                        borderRadius: "100% 0% 49% 51% / 0% 56% 44% 100%  ",
                        transition: "border-radius 500ms ease-in-out,",
                    }}
                >
                    <CardMedia
                        component="img"
                        src={pic}
                        alt="Sample Picture"
                        style={{
                            width: "100%",
                            height: "100%",
                            objectFit: "cover",
                        }}
                    />
                </Card>
            </Box>
        </div>
    );
};

export default MainPage;

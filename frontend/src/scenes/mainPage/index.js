import React from "react";
import { useState } from "react";
import Navbar from "../navbar";
import {
    Box,
    Typography,
    Button,
    Card,
    useMediaQuery,
    CardMedia,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import pic from "../../assets/trader.jpg";

const MainPage = () => {
    const navigate = useNavigate();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");
    const isMobile = !isNonMobileScreens;

    const handleMobileMenuToggle = () => {
        setIsMobileMenuOpen((prev) => !prev);
    };

    const handleNavigate = () => {
        navigate("/konverter");
    };

    return (
        <div style={{ width: "100%", height: "100%", overflow: "hidden" }}>
            <Navbar />

            {!isMobile ? (
                <Box
                    marginTop={"4rem"}
                    marginLeft={"6rem"}
                    position="relative"
                    style={{ height: "calc(100% - 4rem)", overflowY: "hidden" }}
                >
                    <Box width={"40%"}>
                        <Box>
                            <Typography variant="h1">
                                Snadné navigování komplexitami danění akcií.
                                Zjednodušte svá daňová přiznání
                            </Typography>
                        </Box>
                        <Box marginTop={"2rem"}>
                            <Typography variant="h4">
                                Stresují Vás složité každoroční daňová přiznání
                                z prodeje cenných papírů? ShareTaxMax vyřeší
                                všechny problémy za vás a to vše během pár
                                kliknutí.
                            </Typography>
                        </Box>
                        <Box>
                            <Button
                                className="button-36"
                                sx={{
                                    fontSize: "0.9rem",
                                    marginTop: "4rem",
                                }}
                                onClick={handleNavigate}
                            >
                                Pojdmě na to !
                            </Button>
                        </Box>
                    </Box>

                    <Box
                        marginTop={"6rem"}
                        width={"65%"}
                        display={"flex"}
                        style={{ height: "calc(100% - 10rem)" }}
                    >
                        <Box width={"40%"} marginRight={"5rem"}>
                            <Typography variant="h2" marginBottom={"0.8rem"}>
                                Jednoduchost
                            </Typography>
                            <Typography variant="h4">
                                Díky jednoduchému uživatelskému rozhraní
                                jednoduše vyplníte své daňové přiznání bez
                                zdlouhavých a komplikovaných postupů.
                            </Typography>
                        </Box>
                        <Box width={"40%"} marginRight={"5rem"}>
                            <Typography variant="h2" marginBottom={"0.8rem"}>
                                Čas
                            </Typography>
                            <Typography variant="h4">
                                ušetříte čas a stres spojený s vyplňováním
                                složitých daňových přiznání z prodeje cenných
                                papírů díky jeho jednoduchosti a přehlednosti.
                            </Typography>
                        </Box>
                        <Box width={"40%"} marginRight={"5rem"}>
                            <Typography variant="h2" marginBottom={"0.8rem"}>
                                Flexibilita
                            </Typography>
                            <Typography variant="h4">
                                Můžete snadno upravit své daňové přiznání v
                                případě změn nebo dodatečných informací.
                            </Typography>
                        </Box>
                    </Box>
                </Box>
            ) : (
                <Box
                    marginTop={"4rem"}
                    position="relative"
                    display="flex"
                    alignItems="center"
                    flexDirection="column"
                    marginLeft={"1rem"}
                    marginRight={"1rem"}
                    style={{ height: "calc(100% - 4rem)", overflowY: "hidden" }}
                >
                    <Box width={"100%"} textAlign="center">
                        <Typography variant="h1">
                            Snadné navigování komplexitami danění akcií.
                            Zjednodušte svá daňová přiznání
                        </Typography>
                    </Box>
                    <Box width={"100%"} marginTop={"2rem"} textAlign="center">
                        <Typography variant="h4">
                            Stresují Vás složité každoroční daňová přiznání z
                            prodeje cenných papírů? ShareTaxMax vyřeší všechny
                            problémy za vás a to vše během pár kliknutí.
                        </Typography>
                    </Box>

                    <Box width={"80%"} textAlign="center" marginTop={"4rem"}>
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Hello1
                        </Typography>
                        <Typography variant="h4">
                            Lorem ipsum dolor sit amet consectetur adipisicing
                            elit. Fugit placeat est, assumenda tenetur rerum
                            dolorem 1111
                        </Typography>
                    </Box>
                    <Box width={"80%"} textAlign="center" marginTop={"4rem"}>
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Hello2
                        </Typography>
                        <Typography variant="h4">
                            Lorem ipsum dolor sit amet consectetur adipisicing
                            elit. Fugit placeat est, assumenda tenetur rerum
                            dolorem 2222
                        </Typography>
                    </Box>
                    <Box width={"80%"} textAlign="center" marginTop={"4rem"}>
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Hello3
                        </Typography>
                        <Typography variant="h4">
                            Lorem ipsum dolor sit amet consectetur adipisicing
                            elit. Fugit placeat est, assumenda tenetur rerum
                            dolorem 3333
                        </Typography>
                    </Box>
                    <Box
                        width={"100%"}
                        display="flex"
                        flexDirection="column"
                        alignItems="center"
                        padding="3rem"
                    >
                        <Button
                            className="button-36"
                            sx={{
                                fontSize: "1.9rem",
                                width: "fit-content",
                                padding: "2rem",
                            }}
                            onClick={handleNavigate}
                        >
                            Kovertovat CSV
                        </Button>
                    </Box>
                </Box>
            )}

            {/* Obrazek */}
            {!isMobile && (
                <Box
                    position="absolute"
                    top="6rem"
                    left="70rem"
                    transform="translateY(-50%)"
                    height="100%"
                    width="100%"
                    zIndex={-1}
                >
                    <Card
                        sx={{
                            maxWidth: "70%",
                            borderRadius: "100% 0% 49% 51% / 0% 56% 44% 100%  ",
                            transition: "border-radius 500ms ease-in-out",
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
            )}
        </div>
    );
};

export default MainPage;

import React, { useEffect } from "react";
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

    // Overflow hidden 
    useEffect(() => {
        // Add the class to the body element when the component mounts
        document.body.classList.add("overflow-hidden");

        // Remove the class when the component unmounts
        return () => {
            document.body.classList.remove("overflow-hidden");
        };
    }, []); // Empty dependency array ensures this effect runs only once

    return (
        <div
            style={{
                width: "100%",
                height: "100%",
                overflow: "hidden", // Add this line to hide overflow
            }}
        >
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
                                    fontSize: "1.2rem",
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
                        width={"60%"}
                        display={"flex"}
                        style={{
                            height: "calc(100% - 10rem)",
                            minWidth: "60rem",
                        }}
                    >
                        <Box width={"50%"} marginRight={"4rem"}>
                            <Typography variant="h2" marginBottom={"0.8rem"}>
                                Jednoduchost
                            </Typography>
                            <Typography variant="h4">
                                Díky jednoduchému uživatelskému rozhraní
                                jednoduše vyplníte své daňové přiznání bez
                                zdlouhavých a komplikovaných postupů.
                            </Typography>
                        </Box>
                        <Box width={"50%"} marginRight={"4rem"}>
                            <Typography variant="h2" marginBottom={"0.8rem"}>
                                Čas
                            </Typography>
                            <Typography variant="h4">
                                Ušetříte čas a stres spojený s vyplňováním
                                složitých daňových přiznání z prodeje cenných
                                papírů díky jeho jednoduchosti a přehlednosti.
                            </Typography>
                        </Box>
                        <Box width={"50%"}>
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
                    <Box
                        width={"100%"}
                        textAlign="center"
                        sx={{ minWidth: "30rem" }}
                    >
                        <Typography variant="h1">
                            Snadné navigování komplexitami danění akcií.
                            Zjednodušte svá daňová přiznání
                        </Typography>
                    </Box>
                    <Box
                        width={"100%"}
                        marginTop={"2rem"}
                        textAlign="center"
                        sx={{ minWidth: "30rem" }}
                    >
                        <Typography variant="h4">
                            Stresují Vás složité každoroční daňová přiznání z
                            prodeje cenných papírů? ShareTaxMax vyřeší všechny
                            problémy za vás a to vše během pár kliknutí.
                        </Typography>
                    </Box>

                    <Box
                        width={"80%"}
                        textAlign="center"
                        marginTop={"4rem"}
                        sx={{ minWidth: "30rem" }}
                    >
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Jednoduchost
                        </Typography>
                        <Typography variant="h4">
                            Díky jednoduchému uživatelskému rozhraní jednoduše
                            vyplníte své daňové přiznání bez zdlouhavých a
                            komplikovaných postupů.
                        </Typography>
                    </Box>
                    <Box
                        width={"80%"}
                        textAlign="center"
                        marginTop={"4rem"}
                        sx={{ minWidth: "30rem" }}
                    >
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Čas
                        </Typography>
                        <Typography variant="h4">
                            Ušetříte čas a stres spojený s vyplňováním složitých
                            daňových přiznání z prodeje cenných papírů díky jeho
                            jednoduchosti a přehlednosti.
                        </Typography>
                    </Box>
                    <Box
                        width={"80%"}
                        textAlign="center"
                        marginTop={"4rem"}
                        sx={{ minWidth: "30rem" }}
                    >
                        <Typography variant="h2" marginBottom={"0.8rem"}>
                            Flexibilita
                        </Typography>
                        <Typography variant="h4">
                            Můžete snadno upravit své daňové přiznání v případě
                            změn nebo dodatečných informací.
                        </Typography>
                    </Box>
                    <Box
                        width={"100%"}
                        display="flex"
                        flexDirection="column"
                        alignItems="center"
                        padding="2rem"
                        marginTop={"1rem"}
                    >
                        <Button
                            className="button-36"
                            sx={{
                                fontSize: "1.9rem",
                                width: "fit-content",
                                padding: "2.5rem",
                            }}
                            onClick={handleNavigate}
                        >
                            Pojďmě na to
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

import React, { useEffect, useState } from "react";
import Navbar from "../navbar";
import {
    Typography,
    Box,
    Divider,
    Card,
    CardMedia,
    Button,
    useMediaQuery,
    Fab,
    Zoom,
} from "@mui/material";
import trading_1 from "../../assets/trading_1.png";
import trading_2 from "../../assets/trading_2.png";
import trading_3 from "../../assets/trading_3.png";
import trading_4 from "../../assets/trading_4.png";
import { useNavigate } from "react-router-dom";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";

const JakZiskat = () => {
    const navigate = useNavigate();
    const [isMobileMenuToggled, setIsMobileMenuToggled] = useState(false);
    const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");

    const handleConverter = () => {
        navigate("/konverter");
    };

    const handleScrollTop = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const ScrollTopButton = () => {
        const handleScrollTop = () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        };

        return (
            <Fab
                color="primary"
                size="medium"
                aria-label="scroll back to top"
                sx={{
                    position: "fixed",
                    bottom: "2rem",
                    right: "2rem",
                    display: "inline-block",
                    visibility: "visible",
                    opacity: 1,
                    transition: "opacity 0.3s",
                    "&:hover": {
                        opacity: 0.8,
                    },
                }}
                onClick={handleScrollTop}
            >
                <KeyboardArrowUpIcon />
            </Fab>
        );
    };

    useEffect(() => {
        document.body.classList.add("no-overflow-hidden");
        return () => {
            document.body.classList.remove("no-overflow-hidden");
        };
    }, []);

    return (
        <div>
            <Navbar />
            <Box width={isNonMobileScreens ? "60%" : "100%"} mx="auto" mt={4}>
                {/* Introduction */}
                <Typography
                    variant="h2"
                    align="center"
                    fontWeight={700}
                    fontStyle="italic"
                    marginTop={"4rem"}
                >
                    Jak získat data od brokera Trading212
                </Typography>
                <Divider sx={{ my: 2 }} />
                {/* Step 1 */}
                <Box
                    display="flex"
                    alignItems="center"
                    marginTop={5}
                    marginLeft={!isNonMobileScreens && "1rem"}
                    marginRight={!isNonMobileScreens && "1rem"}
                >
                    <Box
                        display="flex"
                        justifyContent="center"
                        alignItems="center"
                        minWidth={40}
                        height={40}
                        borderRadius="50%"
                        bgcolor="blue"
                        color="white"
                        fontSize={20}
                        fontWeight={700}
                    >
                        1
                    </Box>
                    <Box ml={2}>
                        <Typography variant="h4" fontWeight={700}>
                            Krok 1: Získání přístupu k Trading212
                        </Typography>
                        <Typography variant="h5">
                            Otevřete si mobílní aplikaci nebo do svého
                            oblíbeného vyhledavače napište
                            <b> https://www.trading212.com/</b> a přihlašte se.
                        </Typography>
                    </Box>
                </Box>
                {/* Step 2 */}
                <Box
                    display="flex"
                    alignItems="center"
                    marginTop={5}
                    marginLeft={!isNonMobileScreens && "1rem"}
                    marginRight={!isNonMobileScreens && "1rem"}
                >
                    <Box
                        display="flex"
                        justifyContent="center"
                        alignItems="center"
                        minWidth={40}
                        height={40}
                        borderRadius="50%"
                        bgcolor="blue"
                        color="white"
                        fontSize={20}
                        fontWeight={700}
                    >
                        2
                    </Box>
                    <Box ml={2}>
                        <Typography variant="h4" fontWeight={700}>
                            Krok 2: Získání blizších informací o účtu
                        </Typography>
                        <Typography variant="h5">
                            V pravo nahoře uvidíte obdelník s Vaší emailovou
                            adresou. Klikněte na šipečku naznačující rozšíření
                            menu.
                        </Typography>
                    </Box>
                </Box>
                <Box display="flex" justifyContent="center" my={2}>
                    <Card sx={{ width: "100%" }}>
                        <CardMedia
                            component="img"
                            image={trading_1} // Replace with the actual image path
                            alt="Trading212"
                            style={{ maxWidth: "100%", height: "auto" }}
                        />
                    </Card>
                </Box>
                {/* Step 3 */}
                <Box
                    display="flex"
                    alignItems="center"
                    marginTop={5}
                    marginLeft={!isNonMobileScreens && "2rem"}
                >
                    <Box
                        display="flex"
                        justifyContent="center"
                        alignItems="center"
                        width={40}
                        height={40}
                        borderRadius="50%"
                        bgcolor="blue"
                        color="white"
                        fontSize={20}
                        fontWeight={700}
                    >
                        3
                    </Box>
                    <Box ml={2}>
                        <Typography variant="h4" fontWeight={700}>
                            Krok 3: Otevřete kolonku History
                        </Typography>
                    </Box>
                </Box>
                <Box display="flex" justifyContent="center" my={2}>
                    <Card sx={{ width: "100%", maxWidth: "300px" }}>
                        <CardMedia
                            component="img"
                            image={trading_2} // Replace with the actual image path
                            alt="Trading212"
                            style={{ maxWidth: "100%", height: "auto" }}
                        />
                    </Card>
                </Box>
                {/* Step 4 */}
                <Box
                    display="flex"
                    alignItems="center"
                    marginTop={5}
                    marginLeft={!isNonMobileScreens && "2rem"}
                >
                    <Box
                        display="flex"
                        justifyContent="center"
                        alignItems="center"
                        width={40}
                        height={40}
                        borderRadius="50%"
                        bgcolor="blue"
                        color="white"
                        fontSize={20}
                        fontWeight={700}
                    >
                        4
                    </Box>
                    <Box ml={2}>
                        <Typography variant="h4" fontWeight={700}>
                            Krok 4: Klikněte na ikonku stažení dat
                        </Typography>
                        <Typography variant="h5"></Typography>
                    </Box>
                </Box>
                <Box display="flex" justifyContent="center" my={2}>
                    <Card sx={{ width: "100%" }}>
                        <CardMedia
                            component="img"
                            image={trading_3} // Replace with the actual image path
                            alt="Trading212"
                            style={{ maxWidth: "100%", height: "auto" }}
                        />
                    </Card>
                </Box>
                {/* Step 5 */}
                <Box
                    display="flex"
                    alignItems="center"
                    marginTop={5}
                    marginLeft={!isNonMobileScreens && "1rem"}
                    marginRight={!isNonMobileScreens && "1rem"}
                >
                    <Box
                        display="flex"
                        justifyContent="center"
                        alignItems="center"
                        minWidth={40}
                        height={40}
                        borderRadius="50%"
                        bgcolor="blue"
                        color="white"
                        fontSize={20}
                        fontWeight={700}
                    >
                        5
                    </Box>
                    <Box ml={2}>
                        <Typography variant="h4" fontWeight={700}>
                            Krok 5: Vyhrazení časového rozmezí
                        </Typography>
                        <Typography variant="h5">
                            Nyní po Vás bude zažádáno obdbí, které chcete
                            uložit. Berte ovšem na vědomí, že{" "}
                            <b>
                                maximálně lze stáhnout v intervalu jednoho roku!{" "}
                            </b>
                            To ovšem neznamená že si nemůžete stáhnout postupně
                            údaje například od roku 2017 až po 2022. Akorát
                            budou rozprostřeny do 5 různých CSV souborů.
                        </Typography>
                    </Box>
                </Box>
                <Box display="flex" justifyContent="center" my={2}>
                    <Card sx={{ width: "100%" }}>
                        <CardMedia
                            component="img"
                            image={trading_4} // Replace with the actual image path
                            alt="Trading212"
                            style={{ maxWidth: "100%", height: "auto" }}
                        />
                    </Card>
                </Box>
                <Box textAlign="center" marginTop="3rem" paddingBottom={"6rem"}>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleConverter}
                        style={{ marginTop: "1.5rem" }}
                        sx={{
                            fontSize: "2rem",
                        }}
                    >
                        Konvertuj soubory
                    </Button>
                </Box>
            </Box>
            <ScrollTopButton />
        </div>
    );
};

export default JakZiskat;

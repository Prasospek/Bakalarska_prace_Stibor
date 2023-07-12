import React, { useState } from "react";
import {
    AppBar,
    Toolbar,
    Typography,
    IconButton,
    Icon,
    Tooltip,
    Box,
    useMediaQuery,
    Drawer,
    List,
    ListItem,
    ListItemText,
    Divider,
} from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close";
import HelpCenterIcon from "@mui/icons-material/HelpCenter";
import { setMode } from "../../state";
import { useNavigate } from "react-router-dom";
import { useTheme } from "@emotion/react";
import { useDispatch } from "react-redux";

function Navbar() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const theme = useTheme();
    const dark = theme.palette.neutral.dark;

    const handleNavigate = (url) => {
        navigate(url);
        setIsMobileMenuOpen(false);
    };

    const handleMobileMenuToggle = () => {
        setIsMobileMenuOpen((prev) => !prev);
    };

    return (
        <AppBar
            position="static"
            sx={{ backgroundColor: "rgba(38, 173, 217, 0.5)" }}
        >
            <Toolbar>
                <Typography
                    fontWeight="bold"
                    fontSize="clamp(1rem, 2rem, 2.25rem)"
                    onClick={() => handleNavigate("/")}
                    sx={{
                        padding: 1.5,
                        "&:hover": {
                            cursor: "pointer",
                        },
                    }}
                >
                    ShareTaxMax
                </Typography>

                {isNonMobileScreens ? (
                    <Typography
                        variant="body1"
                        component="div"
                        sx={{
                            display: "flex",
                            alignItems: "center",
                            marginLeft: "auto",
                        }}
                    >
                        <Typography
                            variant="body1"
                            component="span"
                            sx={{
                                marginRight: "30px",
                                fontSize: 18,
                                "&:hover": {
                                    cursor: "pointer",
                                    textDecoration: "underline",
                                },
                            }}
                            onClick={() => handleNavigate("/jak-pouzivat")}
                        >
                            Jak používat
                        </Typography>
                        <Typography
                            variant="body1"
                            component="span"
                            sx={{
                                marginRight: "30px",
                                fontSize: 18,
                                "&:hover": {
                                    cursor: "pointer",
                                    textDecoration: "underline",
                                },
                            }}
                            onClick={() => handleNavigate("/broker")}
                        >
                            Brokeři
                        </Typography>
                        <Typography
                            variant="body1"
                            component="span"
                            sx={{
                                marginRight: "30px",
                                fontSize: 18,
                                "&:hover": {
                                    cursor: "pointer",
                                    textDecoration: "underline",
                                },
                            }}
                            onClick={() => handleNavigate("/caste-dotazy")}
                        >
                            Časté dotazy
                        </Typography>
                        <Tooltip
                            sx={{ marginLeft: 9 }}
                            title={
                                <Typography
                                    variant="body1"
                                    sx={{ fontSize: 12 }}
                                >
                                    Potřebujete pomoc nebo máte otázku?
                                </Typography>
                            }
                            placement="bottom"
                        >
                            <IconButton onClick={() => handleNavigate("/help")}>
                                <HelpCenterIcon sx={{ fontSize: 25 }} />
                            </IconButton>
                        </Tooltip>
                    </Typography>
                ) : (
                    <IconButton
                        onClick={handleMobileMenuToggle}
                        sx={{ marginLeft: "auto" }}
                    >
                        {isMobileMenuOpen ? <CloseIcon /> : <MenuIcon />}
                    </IconButton>
                )}

                <IconButton
                    onClick={() => dispatch(setMode())}
                    sx={{ fontSize: "25px", marginLeft: "22px" }}
                >
                    {theme.palette.mode === "dark" ? (
                        <Brightness7Icon sx={{ fontSize: "25px" }} />
                    ) : (
                        <Brightness4Icon
                            sx={{ color: dark, fontSize: "25px" }}
                        />
                    )}
                </IconButton>
            </Toolbar>

            {/* Mobile Menu */}
            {!isNonMobileScreens && (
                <Drawer
                    anchor="right"
                    open={isMobileMenuOpen}
                    onClose={handleMobileMenuToggle}
                >
                    <Box
                        sx={{ width: "250px" }}
                        role="presentation"
                        onClick={handleMobileMenuToggle}
                        onKeyDown={handleMobileMenuToggle}
                    >
                        <List>
                            <ListItem
                                button
                                onClick={() => handleNavigate("/")}
                            >
                                <ListItemText primary="Domů" />
                            </ListItem>
                            <Divider />
                            <ListItem
                                button
                                onClick={() => handleNavigate("/jak-pouzivat")}
                            >
                                <ListItemText primary="Jak používat" />
                            </ListItem>
                            <ListItem
                                button
                                onClick={() => handleNavigate("/broker")}
                            >
                                <ListItemText primary="Brokers" />
                            </ListItem>
                            <ListItem
                                button
                                onClick={() => handleNavigate("/caste-dotazy")}
                            >
                                <ListItemText primary="Časté dotazy" />
                            </ListItem>
                            <Divider />
                            <ListItem
                                button
                                onClick={() => handleNavigate("/help")}
                            >
                                <IconButton
                                    onClick={() => handleNavigate("/help")}
                                >
                                    <HelpCenterIcon sx={{ fontSize: 25 }} />
                                </IconButton>
                                <ListItemText>Pomoc / otázky </ListItemText>
                            </ListItem>
                        </List>
                    </Box>
                </Drawer>
            )}
        </AppBar>
    );
}

export default Navbar;

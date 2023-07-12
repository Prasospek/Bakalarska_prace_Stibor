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
    ListItemIcon,
} from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { Menu, Close, HelpCenter } from "@mui/icons-material";
import { setMode } from "../../state";
import { useDispatch, useSelector } from "react-redux";
import { useTheme } from "@emotion/react";
import HelpCenterIcon from "@mui/icons-material/HelpCenter";
import { useNavigate } from "react-router-dom";

function Navbar() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");

    const dispatch = useDispatch();
    const theme = useTheme();
    const dark = theme.palette.neutral.dark;
    const navigate = useNavigate();

    const handleNavigate = () => {
        navigate("/help");
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
                    onClick={() => navigate("/home")}
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
                            sx={{ marginRight: "30px", fontSize: 18 }}
                        >
                            Jak používat
                        </Typography>
                        <Typography
                            variant="body1"
                            component="span"
                            sx={{ marginRight: "30px", fontSize: 18 }}
                        >
                            Podporované formáty
                        </Typography>
                        <Typography
                            variant="body1"
                            component="span"
                            sx={{ marginRight: "30px", fontSize: 18 }}
                        >
                            Časté dotazy
                        </Typography>
                        <Tooltip
                            sx={{ marginLeft: 15 }}
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
                            <IconButton onClick={handleNavigate}>
                                <HelpCenterIcon sx={{ fontSize: 25 }} />
                            </IconButton>
                        </Tooltip>
                    </Typography>
                ) : (
                    <IconButton
                        onClick={handleMobileMenuToggle}
                        sx={{ marginLeft: "auto" }}
                    >
                        {isMobileMenuOpen ? <Close /> : <Menu />}
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
                            <ListItem button onClick={() => navigate("/home")}>
                                <ListItemText primary="Domů" />
                            </ListItem>
                            <ListItem
                                button
                                onClick={() => navigate("/how-to-use")}
                            >
                                <ListItemText primary="Jak používat" />
                            </ListItem>
                            <ListItem
                                button
                                onClick={() => navigate("/supported-formats")}
                            >
                                <ListItemText primary="Podporované formáty" />
                            </ListItem>
                            <ListItem button onClick={handleNavigate}>
                                <ListItemIcon>
                                    <HelpCenterIcon />
                                </ListItemIcon>
                                <ListItemText primary="Pomocní centrum" />
                            </ListItem>
                        </List>
                    </Box>
                </Drawer>
            )}
        </AppBar>
    );
}

export default Navbar;

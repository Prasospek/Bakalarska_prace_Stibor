import React from "react";
import {
    AppBar,
    Toolbar,
    Typography,
    IconButton,
    Icon,
    Tooltip,
    Box,
} from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { setMode } from "../../state";
import { useDispatch, useSelector } from "react-redux";
import { useTheme } from "@emotion/react";
import HelpCenterIcon from "@mui/icons-material/HelpCenter";
import { useNavigate } from "react-router-dom";

function Navbar() {
    const dispatch = useDispatch();
    const theme = useTheme();
    const dark = theme.palette.neutral.dark;
    const navigate = useNavigate();

    const handleNavigate = () => {
        navigate("http://localhost:8000/help");
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
                        "&:hover": {
                            cursor: "pointer",
                        },
                    }}
                >
                    ShareTaxMax
                </Typography>

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
                        sx={{ marginRight: "16px" }}
                    >
                        Jak používat
                    </Typography>
                    <Typography
                        variant="body1"
                        component="span"
                        sx={{ marginRight: "16px" }}
                    >
                        Podporované formáty
                    </Typography>
                    <Typography
                        variant="body1"
                        component="span"
                        sx={{ marginRight: "16px" }}
                    >
                        Časté dotazy
                    </Typography>
                </Typography>

                <Tooltip
                    sx={{ marginLeft: 15 }}
                    title={
                        <Typography variant="body1" sx={{ fontSize: 12 }}>
                            Potřebujete pomoc nebo máte otázku ?
                        </Typography>
                    }
                    placement="bottom"
                >
                    <IconButton onClick={handleNavigate}>
                        <HelpCenterIcon sx={{ fontSize: 25 }} />
                    </IconButton>
                </Tooltip>

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
        </AppBar>
    );
}

export default Navbar;

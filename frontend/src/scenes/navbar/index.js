import React from "react";
import { AppBar, Toolbar, Typography, IconButton } from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import { setMode } from "../../state";
import { useDispatch, useSelector } from "react-redux";
import { useTheme } from "@emotion/react";

function Navbar() {
    const dispatch = useDispatch();
    const theme = useTheme();
    const dark = theme.palette.neutral.dark;

    return (
        <AppBar position="static">
            <Toolbar>
                <Typography
                    variant="body1"
                    component="div"
                    sx={{ flexGrow: 1 }}
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
                        Contact
                    </Typography>
                </Typography>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Your Logo
                </Typography>
                <IconButton
                    onClick={() => dispatch(setMode())}
                    sx={{ fontSize: "25px" }}
                >
                    {theme.palette.mode === "dark" ? (
                        <Brightness4Icon sx={{ fontSize: "25px" }} />
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

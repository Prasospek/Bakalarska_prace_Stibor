import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";

function Navbar() {
    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Your Logo
                </Typography>
                <Typography
                    variant="body1"
                    component="div"
                    sx={{ marginRight: "16px" }}
                >
                    Home
                </Typography>
                <Typography
                    variant="body1"
                    component="div"
                    sx={{ marginRight: "16px" }}
                >
                    About
                </Typography>
                <Typography
                    variant="body1"
                    component="div"
                    sx={{ marginRight: "16px" }}
                >
                    Contact
                </Typography>
            </Toolbar>
        </AppBar>
    );
}

export default Navbar;

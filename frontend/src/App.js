import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./scenes/mainPage";
import { useMemo } from "react";
import { useSelector } from "react-redux";
import { ThemeProvider, CssBaseline, createTheme } from "@mui/material";
// ThemeProvider -> customization of theme
// cssBaseline -> reset Css
// createTheme -> custon theme
import { themeSettings } from "./theme";
import { Navigate } from "react-router-dom";
import Helper from "./scenes/helper";
import CasteDotazy from "./scenes/casteDotazy";
import JakZiskat from "./scenes/jakZiskat";
import Konverter from "./scenes/konverter";
import React, { useEffect } from "react";

function App() {
    const mode = useSelector((state) => state.mode);
    const theme = useMemo(() => createTheme(themeSettings(mode)), [mode]);
    useEffect(() => {
        document.title = "ShareTaxMax";
    }, []);

    return (
        <ThemeProvider theme={theme}>
            <div className="App">
                <BrowserRouter>
                    <CssBaseline />
                    <Routes>
                        <Route path="/" element={<MainPage />} />
                        <Route path="/help" element={<Helper />} />
                        <Route path="/caste-dotazy" element={<CasteDotazy />} />
                        <Route path="/ziskani-dat" element={<JakZiskat />} />
                        <Route path="/konverter" element={<Konverter />} />

                        {/* Fallback for invalid routes */}
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </BrowserRouter>
            </div>
        </ThemeProvider>
    );
}

export default App;

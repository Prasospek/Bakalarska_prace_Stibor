import "./App.css";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import MainPage from "./scenes/mainPage";
import { useMemo } from "react";
import { useSelector } from "react-redux";
import { ThemeProvider, CssBaseline, createTheme } from "@mui/material";
// ThemeProvider -> customization of theme
// cssBaseline -> reset Css
// createTheme -> custon theme
import { themeSettings } from "./theme";
import { Navigate } from "react-router-dom";

function App() {
    const mode = useSelector((state) => state.mode);
    const theme = useMemo(() => createTheme(themeSettings(mode)), [mode]);

    return (
        <div className="App">
            <BrowserRouter>
                <CssBaseline />
                <ThemeProvider theme={theme}>
                    <Routes>
                        <Route path="/" element={<MainPage />} />
                        {/* Fallback for invalid routes */}
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </ThemeProvider>
            </BrowserRouter>
        </div>
    );
}

export default App;

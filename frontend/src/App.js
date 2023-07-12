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
import Helper from "./scenes/helper";

function App() {
    const mode = useSelector((state) => state.mode);
    const theme = useMemo(() => createTheme(themeSettings(mode)), [mode]);

    return (
        <ThemeProvider theme={theme}>
            <div className="App">
                <BrowserRouter>
                    <CssBaseline />
                    <Routes>
                        <Route path="/" element={<MainPage />} />
                        <Route path="/help" element={<Helper />} />
                        {/* Fallback for invalid routes */}
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </BrowserRouter>
            </div>
        </ThemeProvider>
    );
}

export default App;
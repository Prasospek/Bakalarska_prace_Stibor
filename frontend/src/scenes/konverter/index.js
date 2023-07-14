import React, { useState } from "react";
import {
    Button,
    Container,
    Typography,
    useMediaQuery,
    Link,
    Box,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import Navbar from "../navbar";
import { Link as RouterLink } from "react-router-dom";
import JakPouzivat from "../jakPouzivat";
import { useNavigate } from "react-router-dom";

const Konverter = () => {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [isMobileMenuToggled, setIsMobileMenuToggled] = useState(false);
    const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");
    const navigate = useNavigate();

    const handleJakPouzivat = () => {
        navigate("/jak-pouzivat");
    };

    const handleFileChange = (event) => {
        setSelectedFiles([...event.target.files]);
    };

    const handleFileRemove = (file) => {
        const updatedFiles = selectedFiles.filter((f) => f !== file);
        setSelectedFiles(updatedFiles);
    };

    const handleUpload = () => {
        if (selectedFiles.length > 0) {
            const formData = new FormData();
            for (let i = 0; i < selectedFiles.length; i++) {
                formData.append("csvFiles[]", selectedFiles[i]);
            }

            fetch("/backend/upload", {
                method: "POST",
                body: formData,
            })
                .then((response) => {
                    console.log("Files uploaded successfully!");
                })
                .catch((error) => {
                    console.error("Error uploading files:", error);
                });
        }
    };

    const handleDragOver = (event) => {
        event.preventDefault();
        event.stopPropagation();
    };

    const handleDragEnter = (event) => {
        event.preventDefault();
        event.stopPropagation();
    };

    const handleDrop = (event) => {
        event.preventDefault();
        event.stopPropagation();

        const files = event.dataTransfer.files;
        setSelectedFiles([...selectedFiles, ...files]);
    };

    return (
        <div>
            <Navbar />
            <Container
                maxWidth="md"
                style={{ marginTop: "4rem" }}
                onDragOver={handleDragOver}
                onDragEnter={handleDragEnter}
                onDrop={handleDrop}
            >
                <div
                    style={{
                        border: "2px dashed #888",
                        borderRadius: "8px",
                        padding: "3.5rem",
                        textAlign: "center",
                        cursor: "pointer",
                        marginTop: isNonMobileScreens ? "10rem" : "5rem",
                    }}
                >
                    {selectedFiles.length > 0 ? (
                        selectedFiles.map((file) => (
                            <div
                                key={file.name}
                                style={{
                                    display: "flex",
                                    alignItems: "center",
                                }}
                            >
                                <Typography
                                    variant="body1"
                                    fontWeight="bold"
                                    fontSize="1.1rem"
                                    style={{ margin: 0 }}
                                >
                                    {file.name}
                                </Typography>
                                <Button
                                    variant="outlined"
                                    color="error"
                                    size="small"
                                    onClick={() => handleFileRemove(file)}
                                    style={{ marginLeft: "1rem" }}
                                >
                                    X
                                </Button>
                            </div>
                        ))
                    ) : (
                        <Typography
                            variant="body1"
                            fontSize="1.2rem"
                            style={{ margin: 0 }}
                        >
                            Přetáhněte soubor CSV nebo je vyberte kliknutím na
                            tlačítko.
                        </Typography>
                    )}
                    <input
                        accept=".csv"
                        style={{ display: "none" }}
                        id="csv-file-input"
                        type="file"
                        onChange={handleFileChange}
                        multiple
                    />
                    <Button
                        variant="contained"
                        color="primary"
                        component="label"
                        htmlFor="csv-file-input"
                        style={{ marginTop: "1rem" }}
                    >
                        Vyberte složky
                    </Button>
                </div>
                <Box textAlign="center" marginTop="1.2rem">
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleUpload}
                        disabled={selectedFiles.length === 0}
                        style={{ marginTop: "1.5rem" }}
                        sx={{
                            fontSize: "1.5rem",
                        }}
                    >
                        Konvertuj soubory
                    </Button>
                </Box>
                <Box marginTop="3rem" textAlign="center">
                    <Typography variant="h4">
                        Používáte stránku poprvé? Přečtěte si krátký návod{" "}
                        <Link
                            component={RouterLink}
                            to="/jak-pouzivat"
                            onClick={handleJakPouzivat}
                            sx={{
                                cursor: "pointer",
                                "&:hover": {
                                    textDecoration: "underline",
                                },
                            }}
                        >
                            Jak Používat ShareTaxMax
                        </Link>
                    </Typography>
                </Box>
            </Container>
        </div>
    );
};

export default Konverter;

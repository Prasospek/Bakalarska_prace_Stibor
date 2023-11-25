import React, { useState, useRef } from "react";
import {
    Button,
    Container,
    Typography,
    useMediaQuery,
    Link,
    Box,
} from "@mui/material";
import Navbar from "../navbar";
import { Link as RouterLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const Konverter = () => {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");
    const navigate = useNavigate();
    const fileInputRef = useRef(null);

    const handleZiskaniDat = () => {
        navigate("/ziskani-dat");
    };

    const handleFileChange = (event) => {
        // setSelectedFiles([...event.target.files]);
        const filesArray = Array.from(event.target.files);
        setSelectedFiles(filesArray);
    };

    const handleFileRemove = (file) => {
        const updatedFiles = selectedFiles.filter((f) => f !== file);
        setSelectedFiles(updatedFiles);
    };

    const isValidFiles = (files) => {
        return files.every((file) => file.type === "text/csv");
    };

    const handleTaxesPDF = async () => {
        if (selectedFiles.length > 0 && isValidFiles(selectedFiles)) {
            const formData = new FormData();
            for (let i = 0; i < selectedFiles.length; i++) {
                formData.append("files", selectedFiles[i]);
            }

            try {
                const response = await fetch(
                    "http://localhost:8001/api/process-csv/",
                    {
                        method: "POST",
                        body: formData,
                    }
                );

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = "Generované_PDF.pdf"; //
                    link.click();
                    window.URL.revokeObjectURL(url);
                    console.log("PDF downloaded successfully!");
                    toast.success(`Konverze proběhla v pořádku !`);
                    // Clear the selectedFiles state
                    //setSelectedFiles([]);
                    fileInputRef.current.value = "";
                } else {
                    const errorText = await response.text();
                    toast.error(`Chyba při zpracování souborů ! ${errorText}`);
                    throw new Error("Error při stahování PDF");
                }
            } catch (error) {
                console.error("Error při stahování PDF: ", error);
            }
        } else {
            toast.error(
                "Prosím vyberte validní CSV soubory před generováním PDF."
            );
        }
    };

    const handleMerge = async () => {
        if (selectedFiles.length > 0) {
            const formData = new FormData();
            for (let i = 0; i < selectedFiles.length; i++) {
                formData.append("files", selectedFiles[i]);
            }

            try {
                const response = await fetch(
                    "http://localhost:8001/api/merge-csv/",
                    {
                        method: "POST",
                        body: formData,
                    }
                );

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = "Spojená_CSV_data.csv";
                    link.click();
                    window.URL.revokeObjectURL(url);
                    console.log("File downloaded successfully!");
                    toast.success(`Konverze proběhla v pořádku !`);
                    // Clear the selectedFiles state
                    //setSelectedFiles([]);
                    fileInputRef.current.value = "";
                } else {
                    const errorText = await response.text();
                    toast.error(`Chyba při zpojování souborů ! ${errorText}`);
                    throw new Error("Error při stahování PDF");
                }
            } catch (error) {
                console.error("Error při spojování souborů !", error);
            }
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
                        ref={fileInputRef}
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
                        onClick={handleMerge}
                        disabled={selectedFiles.length === 0}
                        style={{ marginTop: "1.5rem" }}
                        sx={{
                            fontSize: "1.5rem",
                        }}
                    >
                        Spojené CSV soubory
                    </Button>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleTaxesPDF}
                        disabled={selectedFiles.length === 0}
                        style={{ marginTop: "1.5rem" }}
                        sx={{
                            fontSize: "1.5rem",
                            width: "20rem",
                            marginLeft: isNonMobileScreens ? "3rem" : 0, // Add this line
                        }}
                    >
                        Přehled daní PDF
                    </Button>
                </Box>
                <Box marginTop="3rem" textAlign="center">
                    <Typography variant="h4">
                        Používate stránku poprvé? Přečtěte si krátký návod{" "}
                        <Link
                            component={RouterLink}
                            to="/ziskani-dat"
                            onClick={handleZiskaniDat}
                            sx={{
                                cursor: "pointer",
                                position: "relative",
                                "&::after": {
                                    content: "''",
                                    position: "absolute",
                                    bottom: "0",
                                    left: "0",
                                    width: "100%",
                                    height: "2px",
                                    backgroundColor: "currentColor",
                                    transform: "scaleX(0)",
                                    transition: "transform 0.3s",
                                },
                                "&:hover::after": {
                                    transform: "scaleX(1)", // This scales the underline to 100% width on hover
                                },
                            }}
                        >
                            Jak získat data z Trading212
                        </Link>
                    </Typography>
                </Box>
            </Container>
            <ToastContainer />
        </div>
    );
};

export default Konverter;

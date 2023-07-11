import React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "../navbar";

const MainPage = () => {
    const [message, setMessage] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(
                    "http://localhost:8001/api/test/"
                );
                const data = response.data;
                setMessage(data.message);
            } catch (error) {
                console.log("Error: ", error);
            }
        };

        fetchData();
        // eslint-disable-next-line
    }, []);
    return (
        <div>
            <Navbar />
            <h1>{message}</h1>
        </div>
    );
};

export default MainPage;
